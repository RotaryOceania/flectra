# Copyright 2016 Tecnativa  - Antonio Espinosa
# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Membership withdrawal",
    "summary": "Log membership withdrawal reason and date of request",
    "version": "1.0.1.0.0",
    "category": "Association",
    "website": "https://gitlab.com/flectra-community/flectra",
    "author": "Tecnativa, Onestein, Odoo Community Association (OCA), Jamotion GmbH",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["membership_extension"],
    "data": [
        "security/ir.model.access.csv",
        "data/membership_withdrawal_reason_data.xml",
        "views/membership_withdrawal_reason_view.xml",
        "views/res_partner_view.xml",
    ],
}
