{
    'name': 'MetaTrader Management',
    'version': '17.0.0.1',
    'description': 'Metatrader Module',
    'summary': '',
    'author': 'Tri Nguyen (Toby)',
    'license': 'LGPL-3',
    'depends': ["base"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mt_account_views.xml',
        'views/mt_history_views.xml',
        'views/res_config_settings_views.xml',
        'data/service_cron.xml'
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}