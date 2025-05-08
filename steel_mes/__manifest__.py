# -*- coding: utf-8 -*-
{
    'name': 'Steel MES',
    'summary': 'Steel MES',
    'version': '18.0.1.0.0',
    'category': 'Industries',
    'description': '''
        AI can build the most efficient production plan. We offer end2end solution from ERP to MES system, 
        ncluding Order, Inventory, Production, Planing, etc.
    ''',
    'website': 'https://www.kuaihe.tech/',
    'author': 'kuai he',
    'license': 'LGPL-3',
    'support': 'sales@kuaihe.tech',
    # 'live_test_url':'',
    # 'price':,
    # 'currency':'EUR',
    'depends': [
        'base',
        'web',
        'auth_signup',
        'sale'
    ],
    'auto_install': False,
    'application': True,
    'images': ['static/description/banner.png'],
    'data': [
        'data/ir_config_parameter_data.xml',
        'data/mes_config_data.xml',
        'security/ir.model.access.csv',
        'views/mes_menuitem.xml',
        'views/mes_config_views.xml',
        'views/mes_role_views.xml',
        'views/mes_user_views.xml',
        'views/mes_menu_views.xml',
        'views/mes_iframe_action.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml'

    ],

}
