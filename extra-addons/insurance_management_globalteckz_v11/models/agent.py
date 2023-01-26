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

from flectra import fields, models, api, _
from flectra.osv import expression
from flectra.tools.float_utils import float_round as round
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT
from flectra.exceptions import UserError, ValidationError
from datetime import datetime


class Agent_details(models.Model):
    _name = "res.partner"
    _inherit = ['res.partner', 'mail.thread']

    dob = fields.Date(string='Date Of Birth', track_visibility='onchange')
    branch_name = fields.Many2one('res.company', string='Branch', track_visibility='onchange')
    is_agent = fields.Boolean('Agent', default=True, track_visibility='onchange')
    agent_code = fields.Char(string='Agent Code', readonly=True, track_visibility='onchange')
    policy_list = fields.One2many('sale.policy', 'policy_holder', string='Policy List')
    image_small = fields.Binary(string='Image Small')
    image = fields.Binary(string='Image')
    customer = fields.Many2one('res.partner', string='customer')
    supplier = fields.Many2one('res.users', string='Supplier')
    is_customer = fields.Boolean('Is Customer',)
    customer_check = fields.Boolean('Check Customer', compute='_compute_customer_true')

    def _compute_customer_true(self):
        for rec in self:
            print('rec+++++++++>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>+++++++++++', rec)
            print('policy_list++++++++++++++++++++++++++', rec.policy_list)
            if rec.policy_list:
                rec.customer_check = True
                rec.is_customer = True
            else:
                rec.customer_check = False
                rec.is_customer = False



    @api.model
    def create(self, vals):
        if self._context.get('is_agent'):
            vals.update({'is_agent': True})
            # sequence = self.env['res.company'].browse(vals['branch_name']).sq_id
            sequence = self.branch_name
            if sequence:
                vals.update({'agent_code': sequence.next_by_id(), })
        return super(Agent_details, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
