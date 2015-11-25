#from openerp import models,  fields,  api

#class purchase_order_line(models.Model):
#    _inherit = "purchase.order.line" 
#    item_seller_price = fields.Float('Seller Price', size=30)
from openerp.osv import osv,  fields
import openerp.addons.decimal_precision as dp
class purchase_order_line(osv.osv):

       
    _inherit ='purchase.order.line'
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            if line.item_seller_price != 0:
                taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.item_seller_price, line.product_qty, line.product_id, line.order_id.partner_id)
            else:
                taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res

    _columns = {

                 'item_seller_price' : fields.float('Tax Price'),
                 #'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),

                 }

            


class purchase_order(osv.osv):
    _inherit ='purchase.order'

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
               val1 += line.price_subtotal
               unit_price = line.price_unit
               if line.item_seller_price != 0:
                unit_price = line.item_seller_price
               for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, unit_price, line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res
    #def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
    #    res = super(purchase_order, self)._amount_all(cr, uid, ids, field_name, arg, context)
    #    for order in self.browse(cr, uid, ids, context=context):
    #        res[order.id]['amount_total'] += order.frais
    #    return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
    'amount_untaxed': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Untaxed Amount',
        store={
            'purchase.order.line': (_get_order, None, 10),
        }, multi="sums", help="The amount without tax", track_visibility='always'),
    'amount_tax': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Taxes',
        store={
            'purchase.order.line': (_get_order, None, 10),
        }, multi="sums", help="The tax amount"),
    'amount_total': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Total',
        store={
            'purchase.order': (lambda self, cr, uid, ids, c={}: ids, ['frais'], 10),
            'purchase.order.line': (_get_order, None, 10),
        }, multi="sums",help="The total amount"),
    #'frais':fields.float('Frais'),
    'order_line': fields.one2many('purchase.order.line', 'order_id', 'Order Lines',
                                      states={'approved':[('readonly',True)],
                                              'done':[('readonly',True)]},
                                              copy=True),
    }

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        """Collects require data from purchase order line that is used to create invoice line
        for that purchase order line
        :param account_id: Expense account of the product of PO line if any.
        :param browse_record order_line: Purchase order line browse record
        :return: Value for fields of invoice lines.
        :rtype: dict
        """
        return {
            'name': order_line.name,
            'account_id': account_id,
            'price_unit': order_line.price_unit or 0.0,
            'item_seller_price': order_line.item_seller_price,
            'quantity': order_line.product_qty,
            'product_id': order_line.product_id.id or False,
            #'item_seller_price':order_line.item_seller_price,
            'uos_id': order_line.product_uom.id or False,
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            'account_analytic_id': order_line.account_analytic_id.id or False,
            'purchase_line_id': order_line.id,
        }


    def action_invoice_create(self, cr, uid, ids, context=None):
        """Generates invoice for given ids of purchase orders and links that invoice ID to purchase order.
        :param ids: list of ids of purchase orders.
        :return: ID of created invoice.
        :rtype: int
        """
        context = dict(context or {})
        
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')

        res = False
        uid_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        for order in self.browse(cr, uid, ids, context=context):
            context.pop('force_company', None)
            if order.company_id.id != uid_company_id:
                #if the company of the document is different than the current user company, force the company in the context
                #then re-do a browse to read the property fields for the good company.
                context['force_company'] = order.company_id.id
                order = self.browse(cr, uid, order.id, context=context)
            
            # generate invoice line correspond to PO line and link that to created invoice (inv_id) and PO line
            inv_lines = []
            for po_line in order.order_line:
                if po_line.state == 'cancel':
                    continue
                acc_id = self._choose_account_from_po_line(cr, uid, po_line, context=context)
                inv_line_data = self._prepare_inv_line(cr, uid, acc_id, po_line, context=context)
                inv_line_id = inv_line_obj.create(cr, uid, inv_line_data, context=context)
                inv_lines.append(inv_line_id)
                po_line.write({'invoice_lines': [(4, inv_line_id)]})

            # get invoice data and create invoice
            inv_data = self._prepare_invoice(cr, uid, order, inv_lines, context=context)
            inv_id = inv_obj.create(cr, uid, inv_data, context=context)

            # compute the invoice
            inv_obj.button_compute(cr, uid, [inv_id], context=context, set_total=True)

            # Link this new invoice to related purchase order
            order.write({'invoice_ids': [(4, inv_id)]})
            res = inv_id
        return res
from openerp import models, fields, api   
class invoice_line(models.Model):

       
    _inherit ='account.invoice.line'
    item_seller_price = fields.Float('Tax Price')          
    #@api.depends('price_unit','item_seller_price', 'discount', 'invoice_line_tax_id', 'quantity',
    #    'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    #def _compute_price(self):
    #    price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        #if self.item_seller_price != 0:
        #    price = self.item_seller_price * (1 - (self.discount or 0.0) / 100.0)
     #   taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
      #  self.price_subtotal = taxes['total']
      #  if self.invoice_id:
       #     self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)
    
#invoice_line()    
#from openerp.osv import osv,  fields
 #  item_seller_price = fields.Float(string='Seller Price' )
#class purchse_order_line_customize(osv.osv):
 #   _inherit = "purchase.order.line"
  #  _columns = {
   # 'item_seller_price' : fields.float(string='Seller Price'),
    #}
    
    