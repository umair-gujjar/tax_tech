from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from datetime import date, datetime, timedelta
import time
class task_project(osv.Model):
    _inherit = 'project.task'

    def on_change_project_id_task(self, cr, uid, ids, project_id, context=None):
        if not project_id:
            return {}
        project_in_task = self.pool.get('project.project').browse(cr, uid, project_id, context=context)
        descrip_task = project_in_task.description
        #check_use_timesheets = project_in_task.use_timesheets
        #if check_use_timesheets True
        #print descrip_task
        return {
                    'value': {
                    'description': descrip_task,
                }
                }
    def DifferenceInTask(self, cr, uid, ids, InitiateTask, StopTask, context=None):
        res = {}
        if InitiateTask and StopTask:
            dt_st_obj = datetime.strptime(InitiateTask,"%Y-%m-%d %H:%M:%S")
            dt_en_obj = datetime.strptime(StopTask,"%Y-%m-%d %H:%M:%S")
            #S_Date=datetime.datetime.strftime(dt_s_obj, "%Y-%m-%d %H:%M:%S")
            #E_Date=datetime.datetime.strftime(dt_e_obj, "%Y-%m-%d %H:%M:%S")
            timedelta = dt_en_obj - dt_st_obj
            print timedelta
            print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"

            res['DifferenceInTask'] = timedelta
        return {'value': res}

    def MyInitiateTask(self, cr, uid, ids, context=None):
        res = datetime.now()
        TaskInitiate = datetime.strftime(res,"%Y-%m-%d %H:%M:%S")
        print "***********************************##############################"   
        print TaskInitiate
        print res
        print "hahahahahahahahahhahahahahhhhhhhhhhhahahahahahahhaaaaaaaaaaaahhaha"
        data = {'InitiateTask': TaskInitiate}
        print data
        result = self.write(cr, uid, ids, {'InitiateTask': res}, context=context)
        return result

    def MyStopTask(self, cr, uid, ids, context=None):
        res = datetime.now()
        TaskStop = datetime.strftime(res,"%Y-%m-%d %H:%M:%S")
        #difference = TaskStop - MyInitiateTask.TaskInitiate
        print "***********************************##############################"   
        print TaskStop
        print res
        print "hahahahahahahahahhahahahahhhhhhhhhhhahahahahahahhaaaaaaaaaaaahhaha"
        data = {'StopTask': TaskStop}
        print data
        #diff = self.write(cr, uid, ids, {'DifferenceInTask': difference}, context=context)
        result = self.write(cr, uid, ids, {'StopTask': res}, context=context)
        return result
    _columns={
    'work_ids': fields.one2many('project.task.work', 'task_id', 'Work done'),
    'InitiateTask': fields.datetime('InitiateTask'),
    'StopTask': fields.datetime('StopTask'),
    'DifferenceInTask' : fields.char('Diffenence in button'),
    'description' : fields.text('Description'),

    #'DifferenceInTask': fields.function(_DifferenceInTask, string='Diffenence in button', ),

    
    }


    
class task_update(osv.Model):
    _inherit = 'project.task.work'

    #fields
    def STask(self, cr, uid, ids, SDate, EDate, context=None):
        res = {}
        if SDate and EDate:
            dt_s_obj = datetime.strftime(SDate,"%Y-%m-%d %H:%M:%S")
            dt_e_obj = datetime.strftime(EDate,"%Y-%m-%d %H:%M:%S")
            #S_Date=datetime.datetime.strftime(dt_s_obj, "%Y-%m-%d %H:%M:%S")
            #E_Date=datetime.datetime.strftime(dt_e_obj, "%Y-%m-%d %H:%M:%S")
            timedelta = dt_e_obj - dt_s_obj

            res['Diff_date'] = timedelta
        return {'value': res}
    _columns={
    'project_id':fields.many2one('project.project','test of description'),
    'name': fields.char('Work summary'),
    'date': fields.datetime('Date', select="1"),
    'task_id': fields.many2one('project.task', 'Task', ondelete='cascade', required=True, select="1"),
    'hours': fields.float('Time Spent'),
    'user_id': fields.many2one('res.users', 'Done by', required=True, select="1"),
    'company_id': fields.related('task_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
    'entries_col' : fields.integer("No of Entries"),
    'sal_col': fields.integer(string="Salary Per Entries"),
    'total_sal':fields.integer('Total Salary', readonly=True),
    'SDate': fields.datetime('Start Date', readonly=True),
    'EDate': fields.datetime('End Date', readonly=True),
    'Diff_date': fields.char('Diffenence in Time'),
    'InitiateTask': fields.datetime('InitiateTask')


    }

    _defaults = {
                'SDate': '',
                'EDate': '',
     }

    def MyInitiateTask(self, cr, uid, ids, context=None):
        res = {}
        res = datetime.now()
        #TaskInitiate = datetime.strftime(res,"%Y-%m-%d %H:%M:%S")
        #print "***********************************##############################"   
        #print TaskInitiate
        #print res
        #print "hahahahahahahahahhahahahahhhhhhhhhhhahahahahahahhaaaaaaaaaaaahhaha"
        #data = {'InitiateTask': TaskInitiate}
        #print data
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
            #S_Date=datetime.datetime.strftime(dt_s_obj, "%Y-%m-%d %H:%M:%S")
            #E_Date=datetime.datetime.strftime(dt_e_obj, "%Y-%m-%d %H:%M:%S")
            timedelta = dt_e_obj - dt_s_obj

            #res['Diff_date'] = timedelta
            result = self.write(cr, uid, ids, {'Diff_date': timedelta}, context=context)
        #TaskInitiate = datetime.strftime(res,"%Y-%m-%d %H:%M:%S")
        #print "***********************************##############################"   
        #print TaskInitiate
        #print res
        #print "hahahahahahahahahhahahahahhhhhhhhhhhahahahahahahhaaaaaaaaaaaahhaha"
        #data = {'InitiateTask': TaskInitiate}
        #print data

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