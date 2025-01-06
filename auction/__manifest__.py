{
    'name': 'Subasta',
    'category': 'Curso',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Esteban Avila',
    'depends': [
        'contacts',
        'product',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res_partner_data.xml',
        'data/auction_cron.xml',
        'views/res_partner_views.xml',
        'views/auction_register_views.xml',
        'views/auction_bid_views.xml',
        'views/sign_in.xml',
        'views/auction_page.xml', 
        'views/auction_detail_page.xml',
        'views/auction_bid_page.xml',
        'views/auction_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'auction/static/src/**/*',
        ],
    },
    'application': True,
    'installable': True,
}
