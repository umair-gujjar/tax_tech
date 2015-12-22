from openerp.osv import osv,  fields
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_compare

class company(osv.osv):
    _inherit = 'account.tax'


    def compute_t(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, force_excluded=False):
        """
        :param force_excluded: boolean used to say that we don't want to consider the value of field price_include of
            tax. It's used in encoding by line where you don't matter if you encoded a tax with that boolean to True or
            False
        RETURN: {
                'total': 0.0,                # Total without taxes
                'total_included: 0.0,        # Total with taxes
                'taxes': []                  # List of taxes, see compute for the format
            }
        """

        # By default, for each tax, tax amount will first be computed
        # and rounded at the 'Account' decimal precision for each
        # PO/SO/invoice line and then these rounded amounts will be
        # summed, leading to the total amount for that tax. But, if the
        # company has tax_calculation_rounding_method = round_globally,
        # we still follow the same method, but we use a much larger
        # precision when we round the tax amount for each line (we use
        # the 'Account' decimal precision + 5), and that way it's like
        # rounding after the sum of the tax amounts of each line
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        tax_compute_precision = precision
        if taxes and taxes[0].company_id.tax_calculation_rounding_method == 'round_globally':
            tax_compute_precision += 5
        totalin = totalex = round(price_unit * quantity, precision)
        tin = []
        tex = []
        for tax in taxes:
            if not tax.Tax_Included_In_Costprice or force_excluded:
                tex.append(tax)
            else:
                tin.append(tax)
        tin = self._compute(cr, uid, tin, price_unit, quantity, product=product, partner=partner, precision=tax_compute_precision)
        for r in tin:
            #totalex =+ r.get('amount', 0.0)
            totalex += r.get('amount', 0.0)
            #totalex += totale
        totlex_qty = 0.0
        try:
            totlex_qty = totalex/quantity
        except:
            pass
        tex = self._compute(cr, uid, tex, totlex_qty, quantity, product=product, partner=partner, precision=tax_compute_precision)
        for r in tex:
            totalin += r.get('amount', 0.0)
        return {
            'total': totalex,
            'total_included': totalin,
            'taxes': tin + tex
        }

    def _unit_compute_tax(self, cr, uid, taxes, price_unit, product=None, partner=None, quantity=0):
        taxes = self._applicable(cr, uid, taxes, price_unit ,product, partner)
        res = []
        cur_price_unit=price_unit
        for tax in taxes:
            if tax.child_tax_included_in_cost_price:
            # we compute the amount for the current tax object and append it to the result
                data = {'id':tax.id,
                        'name': tax.name,
                        'account_collected_id':tax.account_collected_id.id,
                        'account_paid_id':tax.account_paid_id.id,
                        'account_analytic_collected_id': tax.account_analytic_collected_id.id,
                        'account_analytic_paid_id': tax.account_analytic_paid_id.id,
                        'base_code_id': tax.base_code_id.id,
                        'ref_base_code_id': tax.ref_base_code_id.id,
                        'sequence': tax.sequence,
                        'base_sign': tax.base_sign,
                        'tax_sign': tax.tax_sign,
                        'ref_base_sign': tax.ref_base_sign,
                        'ref_tax_sign': tax.ref_tax_sign,
                        'price_unit': cur_price_unit,
                        'tax_code_id': tax.tax_code_id.id,
                        'ref_tax_code_id': tax.ref_tax_code_id.id,
                }
                res.append(data)
                if tax.type=='percent':
                    amount = cur_price_unit * tax.amount
                    data['amount'] = amount

                elif tax.type=='fixed':
                    data['amount'] = tax.amount
                    data['tax_amount']=quantity
                   # data['amount'] = quantity
                elif tax.type=='code':
                    localdict = {'price_unit':cur_price_unit, 'product':product, 'partner':partner, 'quantity': quantity}
                    eval(tax.python_compute, localdict, mode="exec", nocopy=True)
                    amount = localdict['result']
                    data['amount'] = amount
                elif tax.type=='balance':
                    data['amount'] = cur_price_unit - reduce(lambda x,y: y.get('amount',0.0)+x, res, 0.0)
                    data['balance'] = cur_price_unit

                amount2 = data.get('amount', 0.0)
                if tax.child_ids:
                    if tax.child_depend:
                        latest = res.pop()
                    amount = amount2
                    child_tax = self._unit_compute_tax(cr, uid, tax.child_ids, amount, product, partner, quantity)
                    res.extend(child_tax)
                    for child in child_tax:
                        amount2 += child.get('amount', 0.0)
                    if tax.child_depend:
                        for r in res:
                            for name in ('base','ref_base'):
                                if latest[name+'_code_id'] and latest[name+'_sign'] and not r[name+'_code_id']:
                                    r[name+'_code_id'] = latest[name+'_code_id']
                                    r[name+'_sign'] = latest[name+'_sign']
                                    r['price_unit'] = latest['price_unit']
                                    latest[name+'_code_id'] = False
                            for name in ('tax','ref_tax'):
                                if latest[name+'_code_id'] and latest[name+'_sign'] and not r[name+'_code_id']:
                                    r[name+'_code_id'] = latest[name+'_code_id']
                                    r[name+'_sign'] = latest[name+'_sign']
                                    r['amount'] = data['amount']
                                    latest[name+'_code_id'] = False
                if tax.include_base_amount:
                    cur_price_unit+=amount2
        return res



    def compute_all_tax(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, force_excluded=False):
        """
        :param force_excluded: boolean used to say that we don't want to consider the value of field price_include of
            tax. It's used in encoding by line where you don't matter if you encoded a tax with that boolean to True or
            False
        RETURN: {
                'total': 0.0,                # Total without taxes
                'total_included: 0.0,        # Total with taxes
                'taxes': []                  # List of taxes, see compute for the format
            }
        """

        # By default, for each tax, tax amount will first be computed
        # and rounded at the 'Account' decimal precision for each
        # PO/SO/invoice line and then these rounded amounts will be
        # summed, leading to the total amount for that tax. But, if the
        # company has tax_calculation_rounding_method = round_globally,
        # we still follow the same method, but we use a much larger
        # precision when we round the tax amount for each line (we use
        # the 'Account' decimal precision + 5), and that way it's like
        # rounding after the sum of the tax amounts of each line
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        tax_compute_precision = precision
        if taxes and taxes[0].company_id.tax_calculation_rounding_method == 'round_globally':
            tax_compute_precision += 5
        totalin = totalex = round(price_unit * quantity, precision)
        tin = []
        tex = []
        for tax in taxes:
            if not tax.child_tax_included_in_cost_price or force_excluded:
                tex.append(tax)
            else:
                tin.append(tax)
        tin = self._compute_tax(cr, uid, tin, price_unit, quantity, product=product, partner=partner, precision=tax_compute_precision)
        for r in tin:
            totalex += r.get('amount', 0.0)
        totlex_qty = 0.0
        try:
            totlex_qty = totalex/quantity
        except:
            pass
        tex = self._compute_tax(cr, uid, tex, totlex_qty, quantity, product=product, partner=partner, precision=tax_compute_precision)
        for r in tex:
            totalin += r.get('amount', 0.0)
        return {
            'total': totalex,
            'total_included': totalin,
            'taxes': tin + tex
        }




    def _compute_tax(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, precision=None):
        """
        Compute tax values for given PRICE_UNIT, QUANTITY and a buyer/seller ADDRESS_ID.

        RETURN:
            [ tax ]
            tax = {'name':'', 'amount':0.0, 'account_collected_id':1, 'account_paid_id':2}
            one tax for each tax id in IDS and their children
        """
        if not precision:
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        res = self._unit_compute_tax(cr, uid, taxes, price_unit, product, partner, quantity)
        total = 0.0
        for r in res:
            if r.get('balance',False):
                r['amount'] = round(r.get('balance', 0.0) * quantity, precision) - total
            else:
                r['amount'] = round(r.get('amount', 0.0) * quantity, precision)
                total += r['amount']
        return res


    def _unit_compute_inv_tax(self, cr, uid, taxes, price_unit, product=None, partner=None):
        taxes = self._applicable(cr, uid, taxes, price_unit,  product, partner)
        res = []
        taxes.reverse()
        cur_price_unit = price_unit

        tax_parent_tot = 0.0
        for tax in taxes:
            if (tax.type=='percent') and not tax.include_base_amount and tax.child_tax_included_in_cost_price:
                tax_parent_tot += tax.amount

        for tax in taxes:
            if (tax.type=='fixed') and not tax.include_base_amount and tax.child_tax_included_in_cost_price:
                cur_price_unit -= tax.amount

        for tax in taxes:
            if tax.child_tax_included_in_cost_price:
                if tax.type=='percent':
                    if tax.include_base_amount:
                        amount = cur_price_unit - (cur_price_unit / (1 + tax.amount))
                    else:
                        amount = (cur_price_unit / (1 + tax_parent_tot)) * tax.amount

                elif tax.type=='fixed':
                    amount = tax.amount

                elif tax.type=='code':
                    localdict = {'price_unit':cur_price_unit, 'product':product, 'partner':partner}
                    eval(tax.python_compute_inv, localdict, mode="exec", nocopy=True)
                    amount = localdict['result']
                elif tax.type=='balance':
                    amount = cur_price_unit - reduce(lambda x,y: y.get('amount',0.0)+x, res, 0.0)

                if tax.include_base_amount:
                    cur_price_unit -= amount
                    todo = 0
                else:
                    todo = 1
                res.append({
                    'id': tax.id,
                    'todo': todo,
                    'name': tax.name,
                    'amount': amount,
                    'account_collected_id': tax.account_collected_id.id,
                    'account_paid_id': tax.account_paid_id.id,
                    'account_analytic_collected_id': tax.account_analytic_collected_id.id,
                    'account_analytic_paid_id': tax.account_analytic_paid_id.id,
                    'base_code_id': tax.base_code_id.id,
                    'ref_base_code_id': tax.ref_base_code_id.id,
                    'sequence': tax.sequence,
                    'base_sign': tax.base_sign,
                    'tax_sign': tax.tax_sign,
                    'ref_base_sign': tax.ref_base_sign,
                    'ref_tax_sign': tax.ref_tax_sign,
                    'price_unit': cur_price_unit,
                    'tax_code_id': tax.tax_code_id.id,
                    'ref_tax_code_id': tax.ref_tax_code_id.id,
                })
                if tax.child_ids:
                    if tax.child_depend:
                        del res[-1]
                        amount = price_unit

                parent_tax = self._unit_compute_inv_tax(cr, uid, tax.child_ids, amount, product, partner)
                res.extend(parent_tax)

            total = 0.0
            for r in res:
                if r['todo']:
                    total += r['amount']
            for r in res:
                r['price_unit'] -= total
                r['todo'] = 0
        return res

    def compute_inv_tax(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, precision=None):
        """
        Compute tax values for given PRICE_UNIT, QUANTITY and a buyer/seller ADDRESS_ID.
        Price Unit is a Tax included price

        RETURN:
            [ tax ]
            tax = {'name':'', 'amount':0.0, 'account_collected_id':1, 'account_paid_id':2}
            one tax for each tax id in IDS and their children
        """
        if not precision:
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        res = self._unit_compute_inv_tax(cr, uid, taxes, price_unit, product, partner=None)
        total = 0.0
        for r in res:
            if r.get('balance',False):
                r['amount'] = round(r['balance'] * quantity, precision) - total
            else:
                r['amount'] = round(r['amount'] * quantity, precision)
                total += r['amount']
        return res


    _columns = {
        'Tax_Included_In_Costprice': fields.boolean('Tax included in cost price',
            help="Do cost price include tax?"),
        'child_tax_included_in_cost_price': fields.boolean('Tax included in cost price',
            help="Include child tax also in cost price"),
    }

    _defaults = {
        'Tax_Included_In_Costprice': 0,
    }
class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'
    def _compute_total(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        #account = tax_obj.browse(cr, uid, uid, context)
        #check_tax = account.Tax_Included_In_Costprice
        for line in self.browse(cr, uid, ids, context=context):
          unit_price = line.price_unit
          if line.item_seller_price != 0:
            unit_price = line.item_seller_price
          taxes = tax_obj.compute_all(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, line.order_id.partner_id)
          cur = line.order_id.pricelist_id.currency_id
          test_result =  cur_obj.round(cr, uid, cur, taxes['total_included']-taxes['total'])
          res[line.id] =  test_result
        return res

    def _compute_tot(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        #account = tax_obj.browse(cr, uid, uid, context)
        #check_tax = account.Tax_Included_In_Costprice
        for line in self.browse(cr, uid, ids, context=context):
          unit_price = line.price_unit
          if line.item_seller_price != 0:
            unit_price = line.item_seller_price
          taxes = tax_obj.compute_t(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, line.order_id.partner_id)
          cur = line.order_id.pricelist_id.currency_id
          intitalprice =  cur_obj.round(cr, uid, cur, taxes['total'])
          res[line.id] = intitalprice/line.product_qty
          #unit_price-taxes['total']
        return res
    def _compute_totel(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        #account = tax_obj.browse(cr, uid, uid, context)
        #check_tax = account.Tax_Included_In_Costprice
        for line in self.browse(cr, uid, ids, context=context):
          unit_price = line.price_unit
          check_price = line.compute_checktax_taxprice

          #taxes = tax_obj.compute_t(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, line.order_id.partner_id)
          #cur = line.order_id.pricelist_id.currency_id
          #intitalprice =  cur_obj.round(cr, uid, cur, taxes['total'] )
          res[line.id] =  unit_price + check_price
          #unit_price-taxes['total']
        return res
    def _compute_totel_checktax(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        #account = tax_obj.browse(cr, uid, uid, context)
        #check_tax = account.Tax_Included_In_Costprice
        for line in self.browse(cr, uid, ids, context=context):
          unit_price = line.price_unit
          if line.item_seller_price != 0:
            unit_price = line.item_seller_price
          check_tax = line.child_tax_diff

          #taxes = tax_obj.compute_t(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, line.order_id.partner_id)
          #cur = line.order_id.pricelist_id.currency_id
          #intitalprice =  cur_obj.round(cr, uid, cur, taxes['total'] )
          subtaction_tax=  check_tax - unit_price
          res[line.id] = subtaction_tax
          #unit_price-taxes['total']
        return res
# This is for the functional field
    def _compute_tot_tax(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        #account = tax_obj.browse(cr, uid, uid, context)
        #check_tax = account.Tax_Included_In_Costprice
        for line in self.browse(cr, uid, ids, context=context):
          unit_price = line.price_unit
          if line.item_seller_price != 0:
            unit_price = line.item_seller_price
          taxes = tax_obj.compute_all_tax(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, line.order_id.partner_id)
          cur = line.order_id.pricelist_id.currency_id
          intitalprice =  cur_obj.round(cr, uid, cur, taxes['total'])
          res[line.id] = intitalprice
          #unit_price-taxes['total']
        return res
    _columns = {
    'amount_tax': fields.function(_compute_total, string='Tax Amount', digits_compute= dp.get_precision('Account')),
    #'check_tax': fields.float(string='Checked Tax'),
    'check_tax': fields.function(_compute_tot, string='Checked Tax', digits_compute= dp.get_precision('Account')),
    'checke_tax': fields.function(_compute_totel, string='Cost per Unit', digits_compute= dp.get_precision('Account'), help="Technical field used to record the product cost set by the user during a picking confirmation (when costing method used is 'average price' or 'real'). Value given in company currency and in product uom."),  # as it's a technical field, we intentionally don't provide the digits attribute
    'compute_checktax_taxprice': fields.function(_compute_totel_checktax, string='Subtraction Checked', digits_compute= dp.get_precision('Account')),
    'child_tax_diff': fields.function(_compute_tot_tax, string='Child tax differentiate', digits_compute= dp.get_precision('Account')),
    }
    def onchange_result(self, cr, uid, ids, check_tax, context=None):
        res = {}
        if check_tax:
            res['checke_tax'] = check_tax + unit_price
        return {'value': res}
#    def write(self, cr, uid, ids, vals, context=None):
#        product_testing_compute = self.pool.get('product.product').browse(cr, uid, uid, context=context)
#        product_sup_tax_field = product_testing_compute.supplier_taxes_id
#        print product_testing_compute.name
#        print product_sup_tax_field
#        print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl"

class purchase_order(osv.osv):
    _inherit ='purchase.order'


    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, group_id, context=None):
        ''' prepare the stock move data from the PO line. This function returns a list of dictionary ready to be used in stock.move's create()'''
        product_uom = self.pool.get('product.uom')
        checke_tax = order_line.checke_tax
        if order_line.product_uom.id != order_line.product_id.uom_id.id:
            checke_tax *= order_line.product_uom.factor / order_line.product_id.uom_id.factor
        if order.currency_id.id != order.company_id.currency_id.id:
            #we don't round the price_unit, as we may want to store the standard price with more digits than allowed by the currency
            checke_tax = self.pool.get('res.currency').compute(cr, uid, order.currency_id.id, order.company_id.currency_id.id, checke_tax, round=False, context=context)
        res = []
        move_template = {
            'name': order_line.name or '',
            'product_id': order_line.product_id.id,
            'product_uom': order_line.product_uom.id,
            'product_uos': order_line.product_uom.id,
            'date': order.date_order,
            'date_expected': fields.date.date_to_datetime(self, cr, uid, order_line.date_planned, context),
            'location_id': order.partner_id.property_stock_supplier.id,
            'location_dest_id': order.location_id.id,
            'picking_id': picking_id,
            'partner_id': order.dest_address_id.id,
            'move_dest_id': False,
            'state': 'draft',
            'purchase_line_id': order_line.id,
            'company_id': order.company_id.id,
            'checke_tax': checke_tax,
            'picking_type_id': order.picking_type_id.id,
            'group_id': group_id,
            'procurement_id': False,
            'origin': order.name,
            'route_ids': order.picking_type_id.warehouse_id and [(6, 0, [x.id for x in order.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id':order.picking_type_id.warehouse_id.id,
            'invoice_state': order.invoice_method == 'picking' and '2binvoiced' or 'none',
        }

        diff_quantity = order_line.product_qty
        for procurement in order_line.procurement_ids:
            procurement_qty = product_uom._compute_qty(cr, uid, procurement.product_uom.id, procurement.product_qty, to_uom_id=order_line.product_uom.id)
            tmp = move_template.copy()
            tmp.update({
                'product_uom_qty': min(procurement_qty, diff_quantity),
                'product_uos_qty': min(procurement_qty, diff_quantity),
                'move_dest_id': procurement.move_dest_id.id,  #move destination is same as procurement destination
                'group_id': procurement.group_id.id or group_id,  #move group is same as group of procurements if it exists, otherwise take another group
                'procurement_id': procurement.id,
                'invoice_state': procurement.rule_id.invoice_state or (procurement.location_id and procurement.location_id.usage == 'customer' and procurement.invoice_state=='2binvoiced' and '2binvoiced') or (order.invoice_method == 'picking' and '2binvoiced') or 'none', #dropship case takes from sale
                'propagate': procurement.rule_id.propagate,
            })
            diff_quantity -= min(procurement_qty, diff_quantity)
            res.append(tmp)
        #if the order line has a bigger quantity than the procurement it was for (manually changed or minimal quantity), then
        #split the future stock move in two because the route followed may be different.
        if float_compare(diff_quantity, 0.0, precision_rounding=order_line.product_uom.rounding) > 0:
            move_template['product_uom_qty'] = diff_quantity
            move_template['product_uos_qty'] = diff_quantity
            res.append(move_template)
        return res
    _columns = {
    'order_line': fields.one2many('purchase.order.line', 'order_id', 'Order Lines',
                                      states={'approved':[('readonly',True)],
                                              'done':[('readonly',True)]},
                                              copy=True),
    }

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)
class stock_move(osv.osv):
    _inherit = "stock.move"
    def action_done(self, cr, uid, ids, context=None):
        self.product_price_update_before_done(cr, uid, ids, context=context)
        res = super(stock_move, self).action_done(cr, uid, ids, context=context)
        return res

    


    def product_price_update_before_done(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        tmpl_dict = {}
        for move in self.browse(cr, uid, ids, context=context):
            #adapt standard price on incomming moves if the product cost_method is 'average'
            if (move.location_id.usage == 'supplier') and (move.product_id.cost_method == 'average'):
                product = move.product_id
                prod_tmpl_id = move.product_id.product_tmpl_id.id
                qty_available = move.product_id.product_tmpl_id.qty_available
                if tmpl_dict.get(prod_tmpl_id):
                    product_avail = qty_available + tmpl_dict[prod_tmpl_id]
                else:
                    tmpl_dict[prod_tmpl_id] = 0
                    product_avail = qty_available
                if product_avail <= 0:
                    new_std_price = move.checke_tax
                else:
                    # Get the standard price
                    amount_unit = product.standard_price
                    new_std_price = ((amount_unit * product_avail) + (move.checke_tax * move.product_qty)) / (product_avail + move.product_qty)
                tmpl_dict[prod_tmpl_id] += move.product_qty
                # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
            ctx = dict(context or {}, force_company=move.company_id.id)
            product_obj.write(cr, SUPERUSER_ID, [product.id], {'standard_price': new_std_price}, context=ctx)
    _columns = {
    'checke_tax': fields.float('Unit Price', help="Technical field used to record the product cost set by the user during a picking confirmation (when costing method used is 'average price' or 'real'). Value given in company currency and in product uom."),  # as it's a technical field, we intentionally don't provide the digits attribute

    }

#from openerp import models,  fields,  api
#class purchase_order_line_custom(models.Model):
#    _inherit = "purchase.order.line"
    #@api.one
    #@api.constrains('product_id.supplier_taxes_id')
    #def _check_description(self):
    #    if self.taxes_id == self.product_id.supplier_taxes_id:
    #        self.update()
    #        print taxes_id
    #        print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwWWWWWWWWWW"
    #        raise ValidationError("Fields name and description must be different")
    #    else:
    #       self.taxes_id = self.product_id.supplier_taxes_id
    #        self.update()
    #        print taxes_id
    #        print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwWWWWWWWWWW"
    #pname = fields.Char(compute='_compute_pname')
    #@api.one
    #@api.depends('product_id','product_id.supplier_taxes_id')
    #def _compute_pname(self):
    #    if self.product_id:
    #        self.pname = product_id.supplier_taxes_id
    #        print pname
    #        print "********************************************************"
    #total_computable_tax = fields.char(compute='_compute_total')
    #@api.depends('product_id', 'product_id.supplier_taxes_id')
    #def _compute_total(self):
    #    if product_id:
    #        self.total_computable_tax = self.product_id.supplier_taxes_id
    #        #record.total_computable_tax = record.product_id.supplier_taxes_id
    #        print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    #        #print total_computable_tax
    #@api.multi
    #def write(self, product_id):
    #    pname = self.env['product.product'].browse(product_id)
        #self.taxes_id = pname
        #x_pname = pname.supplier_taxes_id
    #    print pname

        #print x_pname
    #    print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
        #return super(purchase_order_line_custom, self).write(taxes_id)
from openerp import models,  fields,  api
class purchase_order_line_custom(models.Model):
    _inherit = "purchase.order"
    @api.multi
    def do_update_pol(self, product_id):
        all_pol_recs = self.env['purchase.order.line']
        pid_recs = all_pol_recs.browse(product_id)
        #all_product_rec = self.env['product.product'].browse('supplier_taxes_id')

        #pid_recs.write({'taxes_id': all_product_rec})
        #print pid_recs.write({'taxes_id': all_product_rec})
        print "*********************************************"
        #print all_product_rec
        print "*********************************************"
        print pid_recs
        return True