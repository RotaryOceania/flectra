# Copyright 2016-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from flectra import _, api, fields, models
from flectra.exceptions import ValidationError


class AccountPaymentMode(models.Model):
    """This corresponds to the object payment.mode of v8 with some
    important changes. It also replaces the object payment.method
    of the module sale_payment_method of OCA/e-commerce"""

    _name = "account.payment.mode"
    _description = "Payment Modes"
    _order = "name"
    _check_company_auto = True

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env.company,
    )
    bank_account_link = fields.Selection(
        [("fixed", "Fixed"), ("variable", "Variable")],
        string="Link to Bank Account",
        required=True,
        help="For payment modes that are always attached to the same bank "
        "account of your company (such as wire transfer from customers or "
        "SEPA direct debit from suppliers), select "
        "'Fixed'. For payment modes that are not always attached to the same "
        "bank account (such as SEPA Direct debit for customers, wire transfer "
        "to suppliers), you should select 'Variable', which means that you "
        "will select the bank account on the payment order. If your company "
        "only has one bank account, you should always select 'Fixed'.",
    )
    fixed_journal_id = fields.Many2one(
        "account.journal",
        string="Fixed Bank Journal",
        domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]",
        ondelete="restrict",
        check_company=True,
    )
    # I need to explicitly define the table name
    # because I have 2 M2M fields pointing to account.journal
    variable_journal_ids = fields.Many2many(
        comodel_name="account.journal",
        relation="account_payment_mode_variable_journal_rel",
        column1="payment_mode_id",
        column2="journal_id",
        string="Allowed Bank Journals",
        domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]",
    )
    payment_method_id = fields.Many2one(
        "account.payment.method",
        string="Payment Method",
        required=True,
        ondelete="restrict",
    )
    payment_type = fields.Selection(
        related="payment_method_id.payment_type", readonly=True, store=True
    )
    payment_method_code = fields.Char(
        related="payment_method_id.code", readonly=True, store=True
    )
    active = fields.Boolean(default=True)
    note = fields.Text(translate=True)

    @api.onchange("company_id")
    def _onchange_company_id(self):
        self.variable_journal_ids = False
        self.fixed_journal_id = False

    @api.constrains("bank_account_link", "fixed_journal_id", "payment_method_id")
    def bank_account_link_constrains(self):
        for mode in self.filtered(lambda x: x.bank_account_link == "fixed"):
            if not mode.fixed_journal_id:
                raise ValidationError(
                    _(
                        "On the payment mode '%s', the bank account link is "
                        "'Fixed' but the fixed bank journal is not set"
                    )
                    % mode.name
                )
            else:
                if mode.payment_method_id.payment_type == "outbound":
                    if (
                        mode.payment_method_id.id
                        not in mode.fixed_journal_id.outbound_payment_method_ids.ids
                    ):
                        raise ValidationError(
                            _(
                                "On the payment mode '%s', the payment method "
                                "is '%s', but this payment method is not part "
                                "of the payment methods of the fixed bank "
                                "journal '%s'"
                            )
                            % (
                                mode.name,
                                mode.payment_method_id.name,
                                mode.fixed_journal_id.name,
                            )
                        )
                else:
                    if (
                        mode.payment_method_id.id
                        not in mode.fixed_journal_id.inbound_payment_method_ids.ids
                    ):
                        raise ValidationError(
                            _(
                                "On the payment mode '%s', the payment method "
                                "is '%s' (it is in fact a debit method), "
                                "but this debit method is not part "
                                "of the debit methods of the fixed bank "
                                "journal '%s'"
                            )
                            % (
                                mode.name,
                                mode.payment_method_id.name,
                                mode.fixed_journal_id.name,
                            )
                        )

    @api.constrains("company_id", "variable_journal_ids")
    def company_id_variable_journal_ids_constrains(self):
        for mode in self:
            if any(mode.company_id != j.company_id for j in mode.variable_journal_ids):
                raise ValidationError(
                    _(
                        "The company of the payment mode '%s', does not match "
                        "with one of the Allowed Bank Journals."
                    )
                    % mode.name
                )