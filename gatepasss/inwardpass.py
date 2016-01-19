from openerp.osv import osv,fields
from datetime import date, datetime
class inwardpass(osv.Model):
	_name='inwardpass'
	_inherit = ['mail.thread', 'ir.needaction_mixin']
	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	'document_type' : fields.boolean('LC or PO'),
	'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gin' : fields.char('GIN #',size=32 ),
	'lc' : fields.char('LC Ref.#/PO #',size=32),
	'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	'time_in' : fields.datetime('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	'supplier_details': fields.many2one('res.partner','Supplier Details'),
	'inward_id' : fields.one2many('inward','inwardpass_id',string='Details'),
	'remarks' : fields.text('Remarks')
	#'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'inwardpass')
		vals['name']=sequence
		vals['gin'] = sequence
		return super(inwardpass, self).create(cr, uid, vals, context=context)
	_defaults = {
				'gin': lambda obj, cr, uid, context: '/',
	 }
					

class inward(osv.Model):
    _name = 'inward'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'inwardpass_id' : fields.many2one('inwardpass','Item Category'),
    }

class inwardshop(osv.Model):
	_name='inwardshop'
	def on_change_vehicle(self, cr, uid, ids, fleet_vehicle_id, context=None):
		if not fleet_vehicle_id:
			return {}
		vehicle = self.pool.get('fleet.vehicle').browse(cr, uid, fleet_vehicle_id, context=context)
		drive = vehicle.driver_id.id
		print drive
		return {
					'value': {
					'driver': drive,
				}
				}

	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gin' : fields.char('GIN #',size=32 ),
	'srin' : fields.char('SRIN #',size=32),
	'branch' : fields.many2one('stock.location','Branch Name'),
	#'time_out' : fields.date('Time Out', required=True),
	'time_in' : fields.datetime('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	#'supplier_details': fields.char('Supplier Details',size=32),
	'inshop_id' : fields.one2many('inshop','inwardshop_id',string='Details'),
	'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	'driver' : fields.many2one('res.partner','Driver',domain="['|',('customer','=',True),('employee','=',True)]"),
	'remarks' : fields.text('Remarks')
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'inwardshop')
		vals['name']=sequence
		return super(inwardshop, self).create(cr, uid, vals, context=context)
	_defaults = {
				'gin': lambda obj, cr, uid, context: '/', }			
class inshop(osv.Model):
    _name = 'inshop'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'inwardshop_id' : fields.many2one('inwardshop','Item Category'),
    }

class outwardpass(osv.Model):
	_name='outwardpass'
	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	'nature' : fields.boolean('Return or Rejection'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gon' : fields.char('GON #',size=32 ),
	'sron' : fields.char('SRON Ref.',size=32),
	#'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	#'time_in' : fields.date('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	'supplier_details': fields.many2one('res.partner','Supplier Details'),
	'outward_id' : fields.one2many('outward','outwardpass_id',string='Details'),
	#'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	'remarks' : fields.text('Remarks')
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'outwardpass')
		vals['name']=sequence
		return super(outwardpass, self).create(cr, uid, vals, context=context)

class outward(osv.Model):
    _name = 'outward'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'outwardpass_id' : fields.many2one('outwardpass','Item Category'),
    }

class outwardshop(osv.Model):
	_name='outwardshop'
	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gon' : fields.char('GON #',size=32 ),
	'sin' : fields.char('SIN #',size=32 ),
	#'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'driver' : fields.many2one('res.partner','Driver',domain="['|',('customer','=',True),('employee','=',True)]"),
	#'time_in' : fields.date('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	#'supplier_details': fields.char('Supplier Details',size=32),
	'outshop_id' : fields.one2many('outshop','outwardshop_id',string='Details'),
	'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	'show_reference': fields.boolean('Want to put reference ?'),
	'reference_field': fields.char('Reference', size=64),
	'remarks' : fields.text('Remarks')
	}

	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'outwardshop')
		vals['name']=sequence
		return super(outwardshop, self).create(cr, uid, vals, context=context)

	def on_change_vehicle(self, cr, uid, ids, fleet_vehicle_id, context=None):
		if not fleet_vehicle_id:
			return {}
		vehicle = self.pool.get('fleet.vehicle').browse(cr, uid, fleet_vehicle_id, context=context)
		drive = vehicle.driver_id.id
		print drive
		return {
					'value': {
					'driver': drive,
				}
				}
class outshop(osv.Model):
    _name = 'outshop'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'outwardshop_id' : fields.many2one('outwardshop','Item Category'),
    }

class inwardgen(osv.Model):
	_name='inwardgen'
	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gin' : fields.char('GIN #',size=32 ),
	'document_ref' : fields.char('Document Ref #',size=32),
	#'bilty' : fields.char('Bilty ',size=32),
	#'time_out' : fields.date('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	'time_in' : fields.datetime('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	#'supplier_details': fields.char('Supplier Details',size=32),
	'ingen_id' : fields.one2many('ingen','inwardgen_id',string='Details'),
	#'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	'remarks' : fields.text('Remarks')
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'inwardgen')
		vals['name']=sequence
		return super(inwardgen, self).create(cr, uid, vals, context=context)
	_defaults = {
	'gin': lambda obj, cr, uid, context: '/', }
class ingen(osv.Model):
    _name = 'ingen'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'inwardgen_id' : fields.many2one('inwardgen','Item Category'),
    }

class outwardgen(osv.Model):
	_name='outwardgen'
	_columns= {
	'name': fields.char('Name',readonly=True),
	'date' : fields.date('Date', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gon' : fields.char('GON #',size=32 ),
	'document_ref' : fields.char('Document Ref #',size=32),
	#'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	#'time_in' : fields.date('Time In', required=True),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	#'supplier_details': fields.char('Supplier Details',size=32),
	'outgen_id' : fields.one2many('outgen','outwardgen_id',string='Details'),
	#'fleet_vehicle_id' : fields.many2one('fleet.vehicle','Vehicle Registration'),
	'remarks' : fields.text('Remarks')
	}

	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'outwardgen')
		vals['name']=sequence
		return super(outwardgen, self).create(cr, uid, vals, context=context)
class outgen(osv.Model):
    _name = 'outgen'
    _columns= {
    'uom': fields.char('UOM'),
    'qty': fields.char('QTY'),
    'item': fields.char('Item Category'),
    'outwardgen_id' : fields.many2one('outwardgen','Item Category'),
    }

class inwardret(osv.Model):
	_name='inwardret'
	_columns= {
	'name': fields.char('Name',readonly=True),
	#'name': fields.char('Name', size=32),
	'dept': fields.char('Department/Section', size=32),
	'date_out' : fields.date('Date Out', required=True),
	'date_in' : fields.date('Date In', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gin' : fields.char('GIN #',size=32 ),
	'document_ref' : fields.char('Document Ref #',size=32),
	#'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	'time_in' : fields.datetime('Time In', required=True),
	'workers': fields.char('No of Workers',size=32),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	'inret_id' : fields.one2many('inret','inwardret_id',string='Details'),
	'stock_location_id' : fields.many2one('stock.location','Dept'),
	'remarks' : fields.text('Remarks')
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'inwardret')
		vals['name']=sequence
		return super(inwardret, self).create(cr, uid, vals, context=context)
	_defaults = {
	'gin': lambda obj, cr, uid, context: '/', }
class inret(osv.Model):
    _name = 'inret'
    _columns= {
    'item_des': fields.char('Item Description'),
    'brought_in_qty': fields.integer('Brought In QTY'),
    'qty_used': fields.char('QTY Used'),
    'brought_out_qty': fields.integer('Brought Out QTY'),
    'inwardret_id' : fields.many2one('inwardret','Item Category'),
    }

class outwardret(osv.Model):
	_name='outwardret'
	_columns= {
	'name': fields.char('Name',readonly=True),
	'dept': fields.char('Department/Section', size=32),
	'date_out' : fields.date('Date Out', required=True),
	'date_in' : fields.date('Date In', required=True),
	#'document_type' : fields.boolean('LC or PO'),
	#'invoice_ref' : fields.char('Invoice Ref #', size=32),
	'gon' : fields.char('GON #',size=32 ),
	'document_ref' : fields.char('Document Ref #',size=32),
	#'bilty' : fields.char('Bilty ',size=32),
	'time_out' : fields.datetime('Time Out', required=True),
	'vehicle' : fields.char('Vehicle',size=32),
	'time_in' : fields.datetime('Time In', required=True),
	#'workers': fields.char('No of Workers',size=32),
	'vehicle_type' : fields.char('Vehicle Type',size=32),
	'outret_id' : fields.one2many('outret','outwardret_id',string='Details'),
	'stock_location_id' : fields.many2one('stock.location','Dept'),
	'remarks' : fields.text('Remarks')
	}
	def create(self, cr, uid, vals, context=None):
		sequence=self.pool.get('ir.sequence').get(cr, uid, 'outwardret')
		vals['name']=sequence
		return super(outwardret, self).create(cr, uid, vals, context=context)

class outret(osv.Model):
    _name = 'outret'
    _columns= {
    'item_des': fields.char('Item Description'),
    'brought_in_qty': fields.integer('Brought In QTY'),
    #'qty_used': fields.char('QTY Used'),
    'brought_out_qty': fields.integer('Brought Out QTY'),
    'diff': fields.integer('Differenc (If any)', readonly=True),
    'outwardret_id' : fields.many2one('outwardret','Item Category'),
    }
    def onchange_result(self, cr, uid, ids, brought_in_qty, brought_out_qty, context=None):
        res = {}
        if brought_in_qty and brought_out_qty:
            res['diff'] = brought_in_qty - brought_out_qty
        return {'value': res}
    


class fleet_vehicle(osv.Model):
	_inherit="fleet.vehicle"
	_columns= {
     'veh_reg': fields.one2many('inwardshop', 'fleet_vehicle_id', 'Vehicle Registration'),
     }

class stock_warehouse(osv.Model):
	_inherit="stock.location"
