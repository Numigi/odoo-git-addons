# © 2019 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Github Pull Request',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Connector',
    'summary': 'Define what is a github Pull Request as an odoo object.',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/ir_ui_view.xml',
        'views/ir_actions_act_window.xml',
        'views/ir_ui_menu.xml',
    ],
    'installable': True,
}
