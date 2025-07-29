# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Github Events',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Connector',
    'summary': 'Define what is a github event as an odoo object',
    'depends': [
        'base_sparse_field',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/github_event.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
