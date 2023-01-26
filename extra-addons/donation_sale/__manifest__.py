# Copyright 2016-2021 La Cimade (http://www.lacimade.org/)
# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Donation Sale",
    "version": "1.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "summary": "Manage donations in sale orders",
    "author": "La Cimade, Akretion, Odoo Community Association (OCA), Jamotion GmbH",
    "maintainers": ["alexis-via"],
    "website": "https://gitlab.com/flectra-community/flectra",
    "depends": ["donation_base", "sale_management"],
    "data": [
        "data/cron.xml",
        "views/account_move.xml",
        "views/sale_order.xml",
        "views/donation_tax_receipt.xml",
    ],
    "installable": True,
}
