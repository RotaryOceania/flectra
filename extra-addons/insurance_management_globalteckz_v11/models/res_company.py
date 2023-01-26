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

from flectra import api, fields, models, _
from datetime import datetime


class Branch_details(models.Model):
    _name = "res.company"
    _inherit = ['res.company', 'mail.thread']

    branch_code = fields.Char(string='Branch Code', track_visibility='onchange')
    sq_id = fields.Many2one('ir.sequence', string='Sequence Code', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, track_visibility='onchange')
    name = fields.Char(related='partner_id.name', string='Company Name', size=128, required=True, store=True,
                       track_visibility='onchange')
    parent_id = fields.Many2one('res.company', 'Parent Company', index=True, track_visibility='onchange')
    child_ids = fields.One2many('res.company', 'parent_id', 'Child Companies')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, track_visibility='onchange')

    def _create_sequence(self, vals, refund=False):
        print(">>>>>>>>>>>>>>>>>VALS>>>>>>>>>>>>>>>>>", vals)
        # prefix = vals['branch_code']
        prefix = self.branch_code
        seq = {
            'name': vals['name'],
            'code': prefix,
            'implementation': 'no_gap',
            'prefix': str(prefix) + '/',
            'padding': 4,
            'number_increment': 1,
            'use_date_range': True,
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        return self.env['ir.sequence'].create(seq)

    # def _create_sequence(self, vals, refund=False):
    #     """ Create new no_gap entry sequence for every new Journal"""
    #     prefix = self._get_sequence_prefix(vals['code'], refund)
    #     seq = {
    #         'name': refund and vals['name'] + _(': Refund') or vals['name'],
    #         'implementation': 'no_gap',
    #         'prefix': prefix,
    #         'padding': 4,
    #         'number_increment': 1,
    #         'use_date_range': True,
    #     }
    #     if 'company_id' in vals:
    #         seq['company_id'] = vals['company_id']
    #     return self.env['ir.sequence'].create(seq)


@api.model
def create(self, vals):
    vals.update({'sq_id': self.sudo()._create_sequence(vals).id})
    return super(Branch_details, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
