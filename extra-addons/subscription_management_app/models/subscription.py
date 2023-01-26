
import time
from flectra import api, fields, models, _
from flectra.exceptions import UserError


class SubscriptionDocument(models.Model):
    _name = "subscription.document"
    _description = "Subscription Document"

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True, help="If the active field is set to False, it will allow you to hide the subscription document without removing it.")
    model = fields.Many2one('ir.model', 'Object', required=True,ondelete='cascade')
    field_ids = fields.One2many('subscription.document.fields', 'document_id', 'Fields', copy=True)


class SubscriptionDocumentFields(models.Model):
    _name = "subscription.document.fields"
    _description = "Subscription Document Fields"
    _rec_name = 'field'

    field = fields.Many2one('ir.model.fields', 'Field', domain="[('model_id', '=', parent.model)]", ondelete='cascade',required=True)
    value = fields.Selection([('false','False'),('date','Current Date')], 'Default Value', size=40, help="Default value is considered for field when new document is generated.")
    document_id = fields.Many2one('subscription.document', 'Subscription Document', ondelete='cascade')


def _get_document_types(self):
    self.env.cr.execute('select m.model, s.name from subscription_document s, ir_model m WHERE s.model = m.id order by s.name')
    return self.env.cr.fetchall()


class SubscriptionSubscription(models.Model):
    _name = 'subscription.subscription'
    _description = "Subscription"

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', 'Partner')
    user_id = fields.Many2one('res.users', 'User', required=True, default=lambda self: self.env.user)
    interval_number = fields.Integer('Interval Qty', default=1)
    interval_type = fields.Selection([('minutes', 'Minutes'),('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], 'Interval Unit', default='months')
    numbercall = fields.Integer(string='Number of Calls', default=0, help='How many times the method is called,\na negative number indicates no limit.')
    date_init = fields.Datetime('First Date', default=fields.Datetime.now)
    state = fields.Selection([('draft','Draft'),('running','Running'),('done','Done')], 'Status', copy=False, default='draft')
    doc_source = fields.Reference(string='Source Document', selection=_get_document_types, help="User can choose the source document on which he wants to create documents", required=True)
    doc_lines = fields.One2many('subscription.history', 'subscription_id', 'Documents Created', readonly=True, copy=False)
    cron_id = fields.Many2one('ir.cron', 'Cron Job', help="Scheduler which runs on subscription", states={'running':[('readonly',True)], 'done':[('readonly',True)]})
    notes = fields.Text('Notes', help="Description or Summary of Subscription")
    model_id = fields.Many2one('ir.model', string='Model', help='The model object for the field to evaluate')

    def unlink(self):
        for subscription in self:
            if subscription.state=="running":
                raise UserError(_('You cannot delete an active subscription!'))
            subscription.doc_lines.unlink()
        return super(SubscriptionSubscription, self).unlink()

    def start_process(self):
        Cron = self.env['ir.cron']
        for subscription in self:
            subscription_model = self.env.ref('subscription_management_app.model_subscription_subscription').id
            vals = {
                'name': subscription.name,
                'model_id': subscription_model,
                'interval_number': subscription.interval_number,
                'interval_type': subscription.interval_type,
                'numbercall': subscription.numbercall,
                'nextcall': subscription.date_init,
                'priority': 6,
                'user_id': subscription.user_id.id,
                'state': 'code',
                'code': 'model.model_copy('+str(subscription.id)+')',
            }
            ir_cron = Cron.create(vals)
            if ir_cron:
                subscription.update({'cron_id': ir_cron.id, 'state': 'running'})
        return True

    @api.model
    def model_copy(self, subscription):
        subscription_id = self.env['subscription.subscription'].browse(subscription)
        remaining = subscription_id.cron_id.numbercall
        try:
            doc_source_id = subscription_id.doc_source.id
            model_name = subscription_id.doc_source._name
        except:
            raise UserError(_('Please provide another source document.\nThis one does not exist!'))
        default = {'state':'draft'}
        state = 'running'
        # the subscription is over and we mark it as being done
        if remaining == 1:
            state = 'done'
        document_id = self.env[model_name].browse(doc_source_id).copy(default=default)
        self.env['subscription.history'].create({'subscription_id': subscription_id.id,
                                                 'date':time.strftime('%Y-%m-%d %H:%M:%S'),
                                                 'document_id': model_name+','+str(document_id.id)})
        subscription_id.state = state

    def set_done(self):
        for record in self:
            if record.cron_id:
                record.cron_id.active = False
            record.state = 'done'
        return True

    def set_draft(self):
        for record in self:
            record.state = 'draft'
        return True

class SubscriptionHistory(models.Model):
    _name = 'subscription.history'
    _description = "Subscription History"
    _rec_name = 'date'

    date = fields.Datetime('Date')
    subscription_id = fields.Many2one('subscription.subscription', 'Subscription', ondelete='cascade')
    document_id = fields.Reference(string='Source Document', selection=_get_document_types, help="User can choose the source document on which he wants to create documents")
