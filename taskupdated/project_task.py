from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from datetime import date, datetime, timedelta
import time
class task_project(osv.Model): #declaring/creating new class
    _inherit = 'project.task' #inheriting class

    def on_change_project_id_task(self, cr, uid, ids, project_id, context=None): # function for getting description from project to task on change
        if not project_id: # Condition for product_id
            return {}
        project_in_task = self.pool.get('project.project').browse(cr, uid, project_id, context=context) #getting all data from project on basis of product_id
        descrip_task = project_in_task.description #assiging value of description field value in project to descrip_task variable
        # writing the value of descrip_task variable to the field description in task
        return {
                    'value': {
                    'description': descrip_task,
                }
                }
    # creating field in the database
    _columns={
    'work_ids': fields.one2many('project.task.work', 'task_id', 'Work done'),
    'description' : fields.text('Description'),
    }


    
class task_update(osv.Model):
    _inherit = 'project.task.work'

    #fields
    def STask(self, cr, uid, ids, SDate, EDate, context=None):
        res = {}
        if SDate and EDate:
            dt_s_obj = datetime.strftime(SDate,"%Y-%m-%d %H:%M:%S")
            dt_e_obj = datetime.strftime(EDate,"%Y-%m-%d %H:%M:%S")
            timedelta = dt_e_obj - dt_s_obj

            res['Diff_date'] = timedelta
        return {'value': res}
    _columns={
    'project_id':fields.many2one('project.project','test of description'),
    'name': fields.char('Work summary'),
    #'date': fields.datetime('Date', select="1"),
    'task_id': fields.many2one('project.task', 'Task', ondelete='cascade', required=True, select="1"),
    'hours': fields.float('Time Spent'),
    'user_id': fields.many2one('res.users', 'Done by', required=True, select="1"),
    'company_id': fields.related('task_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
    'entries_col' : fields.integer("No of Entries"),
    #'sal_col': fields.integer(string="Salary Per Entries"),
    #'total_sal':fields.integer('Total Salary', readonly=True),
    'SDate': fields.datetime('Start Date', readonly=True),
    'EDate': fields.datetime('End Date', readonly=True),
    'Diff_date': fields.char('Diffenence in Time'),
    'InitiateTask': fields.datetime('InitiateTask')


    }

    _defaults = {
                'SDate': '',
                'EDate': '',
                'Diff_date':lambda obj, cr, uid, context: '/',
     }

    def MyInitiateTask(self, cr, uid, ids, context=None):
        res = {}
        res = datetime.now()
        result = self.write(cr, uid, ids, {'SDate': res}, context=context)
        return result

    def MyFinalTask(self, cr, uid, ids, context=None):
        res = {}
        res = datetime.now()
        finalresult = self.write(cr, uid, ids, {'EDate': res}, context=context)
        brw_obj = self.pool.get('project.task.work').browse(cr, uid, ids, context=context)
        print brw_obj.SDate
        print brw_obj.EDate
        if brw_obj.SDate and brw_obj.EDate:
            dt_s_obj = datetime.strptime(brw_obj.SDate,"%Y-%m-%d %H:%M:%S")
            dt_e_obj = datetime.strptime(brw_obj.EDate,"%Y-%m-%d %H:%M:%S")
            timedelta = dt_e_obj - dt_s_obj
            result = self.write(cr, uid, ids, {'Diff_date': timedelta}, context=context)
        return finalresult, result   

    def onchange_result(self, cr, uid, ids, sal_col, entries_col, context=None):
        res = {}
        if sal_col and entries_col:
            res['total_sal'] = sal_col * entries_col
        return {'value': res}
class task_project_matrials(osv.Model):
    _inherit = 'project.task.materials'
    _columns={
    'description' :fields.char(string='Work summary'),
    'date' :  fields.datetime(string='Date'),
    'hours' : fields.float(string='Time Spent'),
    }

class project_description(osv.Model):
    _inherit = 'project.project'
    _columns={
    'description' :fields.text(string='Work summary'),
    }