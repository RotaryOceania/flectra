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
from flectra.exceptions import UserError, ValidationError
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


# class new_sale_policy(models.Model):
#     _name = 'new.sale.policy'

#     name = fields.Char(string='Type Name')

class supplier_sale_policy(models.Model):
    _name = 'supplier.sale.policy'

    name = fields.Char(string='supplier')


class sale_policy(models.Model):
    _name = 'sale.policy'
    _rec_name = 'policy_number'
    _inherit = 'mail.thread'

    # types = fields.Many2one('new.sale.policy', string='Type')
    policy_holder = fields.Many2one('res.partner', string='Policy Holder Name', states={'done': [('readonly', True)]},
                                    track_visibility='onchange')
    policy_number = fields.Char(string='Policy number', readonly=True, states={'done': [('readonly', True)]},
                                track_visibility='onchange')
    # policy_term = fields.Many2one('account.payment.term', string='Payment Term',required=True ,states={'done':[('readonly',True)]} , track_visibility='onchange')
    policy_term = fields.Selection([
        ('2', 'One-off'),
        ('1', 'Annual')], string='Payment Type', required=True, states={'done': [('readonly', True)]})
    policy_schemes = fields.Many2one('schemes.details', string='Policy Scheme Name', required=True,
                                     states={'done': [('readonly', True)]}, track_visibility='onchange')
    branch_name = fields.Many2one('res.company', string='Branch', states={'done': [('readonly', True)]},
                                  track_visibility='onchange')
    agent_name = fields.Many2one('res.partner', string='Agent name', states={'done': [('readonly', True)]},
                                 track_visibility='onchange')
    duration = fields.Integer(string='Duration in Days:', required=True, states={'done': [('readonly', True)]})
    issu_date = fields.Datetime(string='Policy Issu Date', required=True, states={'done': [('readonly', True)]})
    end_date = fields.Datetime(compute="policy_issudate", store='True', string='Policy End Date', readonly=True)
    emi = fields.Selection([
        ('2', 'One-off'),
        ('1', 'Annual')], string='Premium Type', required=True, states={'done': [('readonly', True)]})
    policy_amount = fields.Char(string='Policy Amount', states={'done': [('readonly', True)]})
    state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')], string='State', default='new', readonly=True, track_visibility='onchange')
    emi_line_ids = fields.One2many('policy.emi.line', 'sale_policy_id', string='Policy Line Ids')
    limit = fields.Char(string='Limit')
    excess = fields.Char(string='Excess')
    travel_days = fields.Char(string='Travel Days')
    travel_days_consumed = fields.Char(string='Travel Days Consumed')
    territory = fields.Char(string='Territory')
    endorsements = fields.Char(string='Endorsements')
    policy_wording = fields.Char(string='Policy Wording')
    note = fields.Char(string='Note')
    # supplier = fields.Many2one('schemes.details',string='Suppliers')
    supplier1 = fields.Many2one('supplier.sale.policy', related='policy_schemes.supplier1', string='Suppliers')
    umrn = fields.Char(related='policy_schemes.unique_market_reference_number', string='UMRN')
    count_po_orders = fields.Integer(compute='get_purchase_orders_count')

    def purchase_order_btn(self):
        po_obj = self.env['purchase.order']
        pass

    def get_purchase_orders_count(self):
        purchase_obj = self.env['purchase.order']
        res = {}
        for po in self:
            po_ids = purchase_obj.search([])
            po.count_po_orders = len(po_ids.ids)
        return res

    def action_get_purchase_orders(self):
        purchase_obj = self.env['purchase.order'].search([])
        action = self.env.ref('purchase.purchase_rfq')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            # 'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'domain': [('id', 'in', purchase_obj.ids)]
        }

        return result

    def confirm_btn(self):
        # try:
        po_obj = self.env['purchase.order']
        pol_obj = self.env['purchase.order.line']
        existing_po_lst = []
        print('\n\n______ def confirm_btn_________', self, self._context)
        print('_________Policy Scheme_______________', self.policy_schemes, self.policy_schemes.product_name)
        print('______BOM______', self.policy_schemes.product_name.bom_ids)
        print('______BOM______', self.policy_schemes.product_name.bom_ids[0])

        self.generate_sequence()
        if self.policy_schemes.product_name.bom_ids[0]:
            if self.policy_schemes.product_name.bom_ids[0].product_tmpl_id.type == 'consu':
                print('bom line +++++++++++++++++++', self.policy_schemes.product_name.bom_ids[0].bom_line_ids)
                for bomLine in self.policy_schemes.product_name.bom_ids[0].bom_line_ids.filtered(
                        lambda a: a.product_id.type == 'service'):
                    print("><><><><><LINE<><><><><><><>", bomLine)
                    print("><><><><><sellerproduct id<><><><><><><>", bomLine.product_id)
                    print("><><><><><seller<><><><><><><>", bomLine.product_id.seller_ids)
                    if bomLine.product_id.seller_ids:
                        pol_dict = {
                            # 'order_id': po_id.id,
                            'product_id': bomLine.product_id.id,
                            'name': bomLine.product_id.name,
                            'product_qty': bomLine.product_qty,
                            'date_planned': datetime.today(),
                            'product_uom': bomLine.product_id.uom_po_id.id,
                            'price_unit': bomLine.product_id.standard_price,
                        }
                        print('bol_dict++++++++++++++++++', pol_dict)

                        vendor_id = [vendor_id.name.id for vendor_id in bomLine.product_id.seller_ids][0]
                        print('vendor_id++++++++++++', vendor_id)
                        existing_po_id = po_obj.search([('partner_id', '=', vendor_id), ('state', '=', 'draft')])
                        print('existing_po_id++++++++++++++++', existing_po_id)
                        if existing_po_id:
                            existing_po_lst.append(existing_po_id)
                            existing_pol_id = [pol for pol in existing_po_id.order_line.filtered(
                                lambda a: a.product_id.id == bomLine.product_id.id)]
                            if existing_pol_id and existing_pol_id[0]:
                                existing_pol_id[0].write(
                                    {'product_qty': (existing_pol_id[0].product_qty + bomLine.product_qty)})
                            else:
                                pol_dict.update({'order_id': existing_po_id.id})
                                pol_obj.create(pol_dict)
                        else:
                            po_dict = {
                                'partner_id': vendor_id,
                                'date_planned': datetime.today(),
                                'sales_policy_id': self.id,
                                'origin': self.policy_number,
                                'order_line': [(0, 0, pol_dict)]
                            }
                            po_id = po_obj.create(po_dict)
                if existing_po_id:
                    origin = existing_po_id.origin + ' ,' + self.policy_number
                    existing_po_id.write({'origin': origin})
        # except Exception as exc:
        #     print("exc>>>>>>>>>>>>>>>", exc)
        self.state = "confirm"

    def action_cancel(self):
        self.state = 'cancel'

    def generate_sequence(self):
        sequence = self.policy_schemes.sq_id
        self.write({
            'policy_number': sequence.next_by_id()
        })

    @api.depends('duration', 'issu_date')
    def policy_issudate(self):
        addyears = self.duration
        if type(self.issu_date) is bool:
            return
        mydate = datetime.strptime(str(self.issu_date), "%Y-%m-%d %H:%M:%S")
        # self.end_date = mydate + relativedelta(years=addyears,days=-1)
        self.end_date = mydate + timedelta(days=addyears)

    @api.onchange('policy_amount')
    def onchange_duration(self):
        min_amount = self.policy_schemes.min_amount
        max_amount = self.policy_schemes.max_amount
        policy_amount = self.policy_amount

        if policy_amount < min_amount and policy_amount > max_amount:
            raise ValidationError(_('Policy amount is Not Between %s  to %s ') % (min_amount, max_amount))

    # def msg_amount(self, cr, uid, ids, context={}):
    def msg_amount(self):
        # obj = self.browse(cr, uid, ids[0])
        min_amount = self.policy_schemes.min_amount
        # min_amount = obj.policy_schemes.min_amount
        # max_amount = obj.policy_schemes.max_amount
        max_amount = self.policy_schemes.max_amount

        return ('Policy amount is Not Between %s  to %s ') % (min_amount, max_amount)

    # def check_policy_amount(self, cr, uid, ids, context={}):
    def check_policy_amount(self):
        # obj = self.browse(cr, uid, ids[0])
        min_amount = self.policy_schemes.min_amount
        # min_amount = obj.policy_schemes.min_amount
        # max_amount = obj.policy_schemes.max_amount
        max_amount = self.policy_schemes.max_amount
        policy_amount = self.policy_amount
        # policy_amount = obj.policy_amount

        if policy_amount < min_amount or policy_amount > max_amount:
            return False
        return True

    @api.onchange('duration')
    def onchange_duration(self):
        min_duration = self.policy_schemes.min_duration
        max_duration = self.policy_schemes.max_duration
        duration = self.duration
        # if duration < min_duration or duration > max_duration:
        #     raise UserError(_('Policy Duration is Not Between %s Year to %s Year ') % (min_duration, max_duration))

    ################NO need to warning so its commented on july13,2020#################
    # def msg_duration(self):
    #     # obj = self.browse(cr, uid, ids[0])
    #     # min_duration = obj.policy_schemes.min_duration
    #     min_duration = self.policy_schemes.min_duration
    #     # max_duration = obj.policy_schemes.max_duration
    #     max_duration = self.policy_schemes.max_duration
    #     return ('Policy Duration is Not Between %s Year to %s Year ') % (min_duration, max_duration)

    # # def check_policy_duration(self, cr, uid, ids, context={}):
    # def check_policy_duration(self):
    #     # obj = self.browse(cr, uid, ids[0])
    #     min_duration = self.policy_schemes.min_duration
    #     # min_duration = obj.policy_schemes.min_duration
    #     # max_duration = obj.policy_schemes.max_duration
    #     max_duration = self.policy_schemes.max_duration
    #     policy_duration = self.duration

    #     if policy_duration < min_duration or policy_duration > max_duration:
    #         return False
    #     return True

    # _constraints = [(check_policy_amount, msg_amount, ["policy_amount"]),(check_policy_duration, msg_duration, ["duration"])]

    @api.depends('duration', 'policy_amount', 'emi')
    def create_emi_line(self):
        print("\n\n___________def create_emi_line____________", )
        # sequence = self.env['schemes.details'].browse(self.policy_schemes.id).sq_id
        # sequence = self.policy_schemes.sq_id
        # print ('sequence________',sequence)
        # self.write({
        #     'policy_number': sequence.next_by_id(),
        #     # 'state': 'done',
        # })
        self.write({'state': 'done'})
        # print("<>><><><>self.emi<><>><><>", self.emi, self.policy_amount)
        # print("<>><><><>self.duration<><>><><>", self.duration)
        total_emi = int(self.emi)
        per_emi_amount = float(self.policy_amount)
        per_emi_amount = round(per_emi_amount, 2)

        if type(self.issu_date) is bool:
            return
        mydate = datetime.strptime(str(self.issu_date), "%Y-%m-%d %H:%M:%S")

        if self.emi == '2':
            add_months = 1
        elif self.emi == '1':
            add_months = 1

        # for i in range(1,total_emi+1):
        emi_start_date = mydate
        emi_end_date = emi_start_date + relativedelta(months=add_months, days=-1)
        mydate = emi_end_date + relativedelta(days=1)

        emi_liens = {
            'sale_policy_id': self.id,
            'emi_no': 1,
            'emi_start_date': emi_start_date,
            'emi_end_date': self.end_date,
            'emi_amount': per_emi_amount

        }
        emi_line_id = self.env['policy.emi.line'].create(emi_liens)

    def create_policy_number(self):
        # sequence = self.env['schemes.details'].browse(self.policy_schemes.id).sq_id
        sequence = self.policy_schemes.sq_id
        self.write({
            'policy_number': sequence.next_by_id(),
        })
        return True

    def view_policy_invoice(self):

        action = self.env.ref('account.action_move_out_invoice_type')
        form = self.env.ref('account.invoice_form', False)
        form_id = form.id if form else False
        tree = self.env.ref('account.invoice_tree', False)
        tree_id = tree.id if tree else False
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            # 'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }

        pick_ids = []
        for line in self.emi_line_ids:
            if line.invoice_id:
                pick_ids += [line.invoice_id.id]

        if len(pick_ids) > 1:
            result['domain'] = "[('id','in'," + str(pick_ids) + ")]"
            result['views'] = [(tree_id, 'tree'), (form_id, 'form')]

        elif len(pick_ids) == 1:
            result['views'] = [(form_id, 'form'), (tree_id, 'tree')]
            result['res_id'] = pick_ids[0]
        return result

    def send_mail_by_wizard(self):
        if self.policy_holder.email == False:
            raise UserError(_("Please add %s's Email addres for send email ") % (self.policy_holder.name))
        else:
            self.ensure_one()
            template = self.env.ref('old_insurance_management.email_template_policy_details', False)
            compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

            ctx = dict(
                default_model='sale.policy',
                default_res_id=self.id,
                default_use_template=bool(template),
                # default_template_id=template.id,
                default_template_id=template and template.id or False,
                default_composition_mode='comment',
                # mark_invoice_as_sent=True,
            )
            return {
                'name': _('Compose Email'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form.id, 'form')],
                'view_id': compose_form.id,
                'target': 'new',
                'context': ctx,
            }


class policy_emi(models.Model):
    _name = 'policy.emi.line'

    sale_policy_id = fields.Many2one('sale.policy', string='Poliocy Id')
    emi_no = fields.Integer(string='Emi No', readonly=True)
    emi_start_date = fields.Date(string='From Date', readonly=True)
    emi_end_date = fields.Date(string='To Date', readonly=True)
    emi_amount = fields.Float(digits=(5, 2), readonly=True)
    emi_payment_date = fields.Date(string='Payment Date')
    invoice_id = fields.Many2one('account.invoice')
    invoice_id_state = fields.Char(string='Invoice State')

    # invoice_id_state = fields.Selection(related='invoice_id.state',store=True,string='Invoice State')
    # account_id = fields.Many2one('account.account', string='Account',
    #                              index=True, ondelete="cascade",
    #                              domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False)]",
    #                              check_company=True,
    #                              tracking=True)

    def view_invoice(self):
        invoice_id = self.invoice_id

        view_ref = self.env['ir.model.data'].get_object_reference('account', 'invoice_form')
        view_id = view_ref[1] if view_ref else False
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Customer Invoice'),
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_id': invoice_id.id,
            'target': 'current'
        }

        return res

    def emi_invoice(self):
        invoice_obj = self.env['account.move']
        inv_fields = invoice_obj.fields_get()
        default_value = invoice_obj.default_get(inv_fields)

        invoice_line = self.env['account.move.line']
        line_f = invoice_line.fields_get()
        default_line = invoice_line.default_get(line_f)
        default_value.update({'partner_id': self.sale_policy_id.policy_holder.id, 'invoice_date': self.emi_start_date,
                              'invoice_payment_term_id': self.sale_policy_id.policy_term})
        invoice = invoice_obj.new(default_value)
        invoice._onchange_partner_id()
        # default_value.update({'account_id': invoice.account_id.id, 'date_due': invoice.date_due})
        inv_id = invoice.create(default_value)

        default_line.update({
            'journal_id': inv_id.id,
            'product_id': self.sale_policy_id.policy_schemes.product_name.id,
            'name': self.sale_policy_id.policy_schemes.product_name.name,
            'price_unit': self.emi_amount,
            'tax_line_id': [(6, 0, [self.sale_policy_id.policy_schemes.tax.id])]
        })
        inv_line = invoice_line.new(default_line)
        inv_line._onchange_product_id()
        # default_line.update({'invoice_id': inv_id.id,
        #    'account_id': inv_line.with_context({'journal_id': inv_id.journal_id.id}).default_account_id()})

        invoice_line.create(default_line)
        inv_id.action_invoice_open()
        self.invoice_id = inv_id.id
        template_obj = self.env.ref('account.email_template_edi_invoice', False)
        template_obj.send_mail(inv_id.id)
        return True

    def policy_invoice_scheduler(self):
        today_date = datetime.now()
        search_ids = self.env['policy.emi.line'].search(
            [('emi_start_date', '<=', today_date), ('invoice_id', '=', False)])

        for i in search_ids:
            i.emi_invoice()
        return True

    def create(self, vals):
        return super(policy_emi, self.with_context(mail_create_nolog=True)).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
