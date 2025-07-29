# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numistore',
    'version': "14.0.1.0.1",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Listing of odoo modules in the erp',
    'depends': [
        "github_connector",  # TA#16289
        "github_connector_oca",  # TA#16289
        "github_connector_odoo",  # TA#16289
        'mail',
    ],
    'data': [
        'views/odoo_module.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
