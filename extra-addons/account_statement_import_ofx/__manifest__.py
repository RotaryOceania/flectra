{
    "name": "Import OFX Bank Statement",
    "category": "Banking addons",
    "version": "2.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo SA,"
    "Akretion,"
    "La Louve,"
    "GRAP,"
    "Nicolas JEUDY,"
    "Le Filament,"
    "Odoo Community Association (OCA)",
    "website": "https://gitlab.com/flectra-community/bank-statement-import",
    "depends": ["account_statement_import"],
    "data": ["views/account_statement_import.xml"],
    "external_dependencies": {"python": ["ofxparse"]},
    "installable": True,
}
