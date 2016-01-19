from openerp import models,  fields,  api
import datetime
from datetime import date, datetime, timedelta
import time
import math
class account_anlytic_line_inherit(models.Model):
    _inherit='account.analytic.line'
    task_hourly_entries = fields.Integer('Hourly Entries')
    task_fixed_entries = fields.Integer('Fixed Entries')
    task_assigned_to = fields.Many2one('res.users','Task Assigned To')
    hours_materials = fields.Float('Fixed Hours')
    task_assigned_name = fields.Many2one('project.task','Task Name')
    total_no_of_hours = fields.Float('Total Hours')
    overtime_amount_field = fields.Float('Over Time')
    #overtime_amount = fields.Float('Over Time')
    @api.multi
    def recalculate_amount(self):
        analytic_product_amount =  self.product_id.standard_price
        analytic_quantity = self.unit_amount
        current_amount = self.amount
        if current_amount < 0:
            negative_amount = -1 * current_amount
            divide_amount = current_amount/negative_amount
            self.amount =  divide_amount * analytic_product_amount * analytic_quantity
        elif current_amount > 0:
            divide_amount = current_amount/current_amount
            self.amount =  divide_amount * analytic_product_amount * analytic_quantity
        else:
            self.amount = analytic_product_amount * analytic_quantity
    @api.one
    def overtime_amount(self):
        analytic_product_amount =  self.product_id.standard_price
        analytic_quantity = self.unit_amount
        current_amount = self.amount
        overtime_amount_bonus = self.overtime_amount_field
        if current_amount < 0:
            negative_amount = -1 * current_amount
            divide_amount = current_amount/negative_amount
            self.amount =  divide_amount * analytic_product_amount * analytic_quantity * overtime_amount_bonus
        elif current_amount > 0:
            divide_amount = current_amount/current_amount
            self.amount =  divide_amount * analytic_product_amount * analytic_quantity * overtime_amount_bonus
        else:
            self.amount =  analytic_product_amount * analytic_quantity * overtime_amount_bonus    



class Task(models.Model):
    _inherit = "project.task"
    @api.multi
    def write(self, material_ids):
        for task in self:
            res = super(Task, self).write(material_ids)
            if task.material_ids:
                task.analytic_line_ids.unlink()
                task.material_ids.create_analytic_line()
        return res
    def delete_button_analytic(self, material_ids):
        for task in self:
            res = super(Task, self).write(material_ids)
            if task.material_ids:
                task.analytic_line_ids.unlink()
        return res
    @api.multi
    def unlink(self):
        #self.unlink_stock_move()
        self.analytic_line_ids.unlink()
        return super(Task, self).unlink()

class task_project_matrials_customize(models.Model):
    _inherit='project.task.materials'
    def _prepare_analytic_line(self):
        product = self.product_id
        company_id = self.env['res.company']._company_default_get(
            'account.analytic.line')
        journal = self.env.ref(
            'project_task_materials_stock.analytic_journal_sale_materials')
        analytic_account = getattr(self.task_id, 'analytic_account_id', False)\
            or self.task_id.project_id.analytic_account_id
        #test_date = datetime.strftime(self.date,"%Y-%m-%d %H:%M:%S")
        res = {
            'user_id': self.done_by.id,
            'hours_materials' : self.hours,
            'task_assigned_name' : self.task_id.id,
            'name': self.task_id.name + ': ' + self.description,
            'ref': self.task_id.name,
            'date': self.test_date,
            'product_id': product.id,
            'journal_id': journal.id,
            'unit_amount': self.quantity,
            'account_id': analytic_account.id,
        }
        analytic_line_obj = self.pool.get('account.analytic.line')
        amount_dic = analytic_line_obj.on_change_unit_amount(
            self._cr, self._uid, self._ids, product.id, self.uos_qty(),
            company_id, False, journal.id, self._context)
        res.update(amount_dic['value'])
        res['product_uom_id'] = self.product_uom.id
        to_invoice = getattr(self.task_id.project_id.analytic_account_id,
                             'to_invoice', None)
        if to_invoice is not None:
            res['to_invoice'] = to_invoice.id
        return res
    @api.multi
    def create_analytic_line(self):
        for line in self:
            move_id = self.env['account.analytic.line'].create(
                line._prepare_analytic_line())
            line.analytic_line_id = move_id.id
import time
import datetime

from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
class project_work(osv.osv):
    _inherit = "project.task.work"

    def get_user_related_details(self, cr, uid, user_id):
        res = {}
        emp_obj = self.pool.get('hr.employee')
        emp_id = emp_obj.search(cr, uid, [('user_id', '=', user_id)])
        if not emp_id:
            user_name = self.pool.get('res.users').read(cr, uid, [user_id], ['name'])[0]['name']
            raise osv.except_osv(_('Bad Configuration!'),
                 _('Please define employee for user "%s". You must create one.')% (user_name,))
        emp = emp_obj.browse(cr, uid, emp_id[0])
        if not emp.product_id:
            raise osv.except_osv(_('Bad Configuration!'),
                 _('Please define product and product category property account on the related employee.\nFill in the HR Settings tab of the employee form.'))

        if not emp.journal_id:
            raise osv.except_osv(_('Bad Configuration!'),
                 _('Please define journal on the related employee.\nFill in the HR Settings tab of the employee form.'))

        acc_id = emp.product_id.property_account_expense.id
        if not acc_id:
            acc_id = emp.product_id.categ_id.property_account_expense_categ.id
            if not acc_id:
                raise osv.except_osv(_('Bad Configuration!'),
                        _('Please define product and product category property account on the related employee.\nFill in the HR Settings of the employee form.'))

        res['product_id'] = emp.product_id.id
        res['journal_id'] = emp.journal_id.id
        res['general_account_id'] = acc_id
        res['product_uom_id'] = emp.product_id.uom_id.id
        return res

    def _create_analytic_entries(self, cr, uid, vals, context):
        """Create the hr analytic timesheet from project task work"""
        timesheet_obj = self.pool['hr.analytic.timesheet']
        task_obj = self.pool['project.task']

        vals_line = {}
        timeline_id = False
        acc_id = False

        task_obj = task_obj.browse(cr, uid, vals['task_id'], context=context)
        result = self.get_user_related_details(cr, uid, vals.get('user_id', uid))
        vals_line['name'] = '%s: %s' % (tools.ustr(task_obj.name), tools.ustr(vals['name'] or '/'))
        vals_line['user_id'] = vals['user_id']
        vals_line['task_assigned_name'] = task_obj.id
        vals_line['task_fixed_entries'] = vals['entries_col']
        vals_line['product_id'] = result['product_id']
        #if vals.get('date'):
        #    if len(vals['date']) > 10:
        #        timestamp = datetime.datetime.strptime(vals['date'], tools.DEFAULT_SERVER_DATETIME_FORMAT)
        #        ts = fields.datetime.context_timestamp(cr, uid, timestamp, context)
        #        vals_line['date'] = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        #    else:
        #        vals_line['date'] = vals['date']

        # Calculate quantity based on employee's product's uom
        vals_line['unit_amount'] = vals['hours']

        default_uom = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.project_time_mode_id.id
        if result['product_uom_id'] != default_uom:
            vals_line['unit_amount'] = self.pool['product.uom']._compute_qty(cr, uid, default_uom, vals['hours'], result['product_uom_id'])
        acc_id = task_obj.project_id and task_obj.project_id.analytic_account_id.id or acc_id
        if acc_id:
            vals_line['account_id'] = acc_id
            res = timesheet_obj.on_change_account_id(cr, uid, False, acc_id)
            if res.get('value'):
                vals_line.update(res['value'])
            vals_line['general_account_id'] = result['general_account_id']
            vals_line['journal_id'] = result['journal_id']
            vals_line['amount'] = 0.0
            vals_line['product_uom_id'] = result['product_uom_id']
            amount = vals_line['unit_amount']
            prod_id = vals_line['product_id']
            unit = False
            timeline_id = timesheet_obj.create(cr, uid, vals=vals_line, context=context)

            # Compute based on pricetype
            amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, timeline_id,
                prod_id, amount, False, unit, vals_line['journal_id'], context=context)
            if amount_unit and 'amount' in amount_unit.get('value',{}):
                updv = { 'amount': amount_unit['value']['amount'] }
                timesheet_obj.write(cr, uid, [timeline_id], updv, context=context)

        return timeline_id

    def write(self, cr, uid, ids, vals, context=None):
        """
        When a project task work gets updated, handle its hr analytic timesheet.
        """
        if context is None:
            context = {}
        timesheet_obj = self.pool.get('hr.analytic.timesheet')
        uom_obj = self.pool.get('product.uom')
        result = {}

        if isinstance(ids, (long, int)):
            ids = [ids]

        for task in self.browse(cr, uid, ids, context=context):
            line_id = task.hr_analytic_timesheet_id
            if not line_id:
                # if a record is deleted from timesheet, the line_id will become
                # null because of the foreign key on-delete=set null
                continue

            vals_line = {}
            if 'name' in vals:
                vals_line['name'] = '%s: %s' % (tools.ustr(task.task_id.name), tools.ustr(vals['name'] or '/'))
                #vals_line['task_assigned_name'] = '%s' % (tools.ustr(task.task_id.name))
            if 'entries_col' in vals:
                vals_line['task_fixed_entries'] = vals['entries_col']
            if 'user_id' in vals:
                vals_line['user_id'] = vals['user_id']
            if 'date' in vals:
                vals_line['date'] = vals['date'][:10]
            if 'hours' in vals:
                vals_line['unit_amount'] = vals['hours']
                prod_id = vals_line.get('product_id', line_id.product_id.id) # False may be set

                # Put user related details in analytic timesheet values
                details = self.get_user_related_details(cr, uid, vals.get('user_id', task.user_id.id))
                for field in ('product_id', 'general_account_id', 'journal_id', 'product_uom_id'):
                    if details.get(field, False):
                        vals_line[field] = details[field]

                # Check if user's default UOM differs from product's UOM
                user_default_uom_id = self.pool.get('res.users').browse(cr, uid, uid).company_id.project_time_mode_id.id
                if details.get('product_uom_id', False) and details['product_uom_id'] != user_default_uom_id:
                    vals_line['unit_amount'] = uom_obj._compute_qty(cr, uid, user_default_uom_id, vals['hours'], details['product_uom_id'])

                # Compute based on pricetype
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, line_id.id,
                    prod_id=prod_id, company_id=False,
                    unit_amount=vals_line['unit_amount'], unit=False, journal_id=vals_line['journal_id'], context=context)

                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    vals_line['amount'] = amount_unit['value']['amount']

            if vals_line:
                self.pool.get('hr.analytic.timesheet').write(cr, uid, [line_id.id], vals_line, context=context)

        return super(project_work,self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, *args, **kwargs):
        hat_obj = self.pool.get('hr.analytic.timesheet')
        hat_ids = []
        for task in self.browse(cr, uid, ids):
            if task.hr_analytic_timesheet_id:
                hat_ids.append(task.hr_analytic_timesheet_id.id)
        # Delete entry from timesheet too while deleting entry to task.
        if hat_ids:
            hat_obj.unlink(cr, uid, hat_ids, *args, **kwargs)
        return super(project_work,self).unlink(cr, uid, ids, *args, **kwargs)

    _columns={
        'hr_analytic_timesheet_id':fields.many2one('hr.analytic.timesheet','Related Timeline Id', ondelete='set null'),
    }

from openerp import models,  fields,  api
class project_view_form_button(models.Model):
    _inherit = "project.project"
    @api.multi
    def do_update_des(self):
        print self.description
        prj_des = self.description
        for task_all in self.tasks:
            task_all.description = prj_des
            print task_all.description



from openerp import models,  fields,  api
class product_in_ptm_line(models.Model):
    _inherit = "project.task.materials"
    @api.onchange('product_id','quantity')
    def onchange_product_hours(self):
        product_in_project_line = self.product_id.standard_price
        self.amount_recalculate = product_in_project_line * self.quantity

class product_in_ptw_line(models.Model):
    _inherit = "project.task.work"
    @api.onchange('hours')
    def onchange_product_hours(self):
        test = self.user_id
        emp_obj_all = self.env['hr.employee']
        emp_obj_id = emp_obj_all.search([])
        for each_emp in emp_obj_id:
            if each_emp.user_id == test:
                product_price = each_emp.product_id.standard_price
                print product_price
        self.amount_recalculate = product_price * self.hours

