# -*- coding: utf-8 -*-
##############################################################################
#
#    Globalteckz Pvt Ltd
#    Copyright (C) 2013-Today(www.globalteckz.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from flectra import fields, models ,api, _
from datetime import datetime
from flectra.exceptions import UserError, ValidationError

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'

#     supplier1 = fields.Many2one('supplier.sale.policy',string='Suppliers')
#     umrn = fields.Char(string='UMRN')

class policy_structure(models.Model):
    _name = 'policy.details'
    _rec_name = 'name'
    _description = "Policy Details"
    _inherit =  'mail.thread'

    name = fields.Char(string = 'Policy Name:',track_visibility='onchange')
    policy_code = fields.Char(string = 'Policy Code:',track_visibility='onchange')

class policy_schemes(models.Model):
    _name = 'schemes.details'
    _inherit = 'mail.thread'

    product_name = fields.Many2one('product.product',string='Product Name:', required=True,track_visibility='onchange')
    name = fields.Char(string='Schemes Name', required=True,track_visibility='onchange')
    policy_type = fields.Many2one('policy.details',string = 'Policy Type:',required=True,track_visibility='onchange')
    schemes_code = fields.Char(string = 'Policy Code:',required=True,track_visibility='onchange')
    min_amount = fields.Float(string = 'Minimum Amount:',track_visibility='onchange')
    max_amount = fields.Float(string = 'Maximum Amount:',track_visibility='onchange')
    tax = fields.Many2one('account.tax',string = 'Tax:',track_visibility='onchange')
    intrest_rate = fields.Float(string = 'Interest rate:',track_visibility='onchange')
    min_duration = fields.Integer(string = 'Minimum Duration:',track_visibility='onchange')
    max_duration = fields.Integer(string = 'Maximum Duration:',track_visibility='onchange')
    agents = fields.Many2many('res.partner',string = 'Agents:',track_visibility='onchange')
    sq_id = fields.Many2one('ir.sequence',string='Sequence Code', readonly=True,track_visibility='onchange')
    supplier = fields.Char(string='Supplier')
    supplier1 = fields.Many2one('supplier.sale.policy',string='Suppliers')
    unique_market_reference_number = fields.Char(string='UMRN')


    def _create_sequence(self, vals, refund=False):
        prefix = vals['schemes_code']
        seq = {
                'name': vals['name'],
                'code': prefix,
                'implementation': 'no_gap',
                'prefix': prefix+'/',
                'padding': 4,
                'number_increment': 1,
                'use_date_range': True,
                }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        return self.env['ir.sequence'].create(seq)
    
    @api.model
    def create(self, vals):
        vals.update({'sq_id': self.sudo()._create_sequence(vals).id})
        res = super(policy_schemes, self).create(vals)
        if res.min_duration <= 0 or res.max_duration < res.min_duration:
            raise ValidationError(_("Please Set Minimum and Maximum Duration, And it should be greater than Zero/0."))
        return res

    # @api.model
    def write(self, vals):
        min_duration = vals.get('min_duration')
        max_duration = vals.get('max_duration')
        # if min_duration != None or max_duration < min_duration:
        if min_duration != None:

            raise ValidationError(_("Please Set Minimum and Maximum Duration, And it should be greater than Zero/0."))
        return super(policy_schemes, self).write(vals)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
