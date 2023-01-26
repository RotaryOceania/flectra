from flectra import api,fields,models

class new_sale_policy(models.Model):
    _inherit = 'purchase.order'

    sales_policy_id = fields.Many2one('sale.policy',string='Sales Policy')
    supplier1 = fields.Many2one('supplier.sale.policy',string='Suppliers')
    umrn = fields.Char(string='UMRN')
    picking_count = fields.Integer(string='Picking Count')
    picking_ids = fields.Many2many('stock.picking',string='Picking Ids')
    is_shipped = fields.Boolean(string='Is Shipped')
    on_time_rate = fields.Float(string='On Time Rate')
    effective_date = fields.Datetime(string='Effective Date')
    picking_type_id = fields.Many2one('stock.picking.type',string='Picking Type Id')
    default_location_dest_id_usage = fields.Selection([
        ('one off', 'One-off'),
        ('annual', 'Annual')], string='Default Location Dest Id Usage ')

    # default_location_dest_id_usage = fields.selection([
    #         ('new', 'New'),
    #         ('confirm', 'Confirm'),
    #         ('cancel', 'Cancelled'),
    #         ('done', 'Done')],string='default location dest id usage')
