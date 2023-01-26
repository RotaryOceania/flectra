# Copyright 2014-2021 Barroux Abbey (http://www.barroux.org)
# Copyright 2014-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Donation Recurring",
    "version": "1.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "summary": "Manage recurring donations",
    "author": "Barroux Abbey, Akretion, Odoo Community Association (OCA), Jamotion GmbH",
    "maintainers": ["alexis-via"],
    "website": "https://gitlab.com/flectra-community/flectra",
    "depends": [
        "donation",
    ],
    "data": [
        "views/donation.xml",
        "wizard/donation_recurring_generate_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/donation_recurring_demo.xml"],
    "installable": True,
}
