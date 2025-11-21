{
    'name': 'Delivery Product Images',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Show product images in delivery order forms',
    'description': """
        This module adds product images to delivery order form views.
        Images are displayed in the product lines for better visual identification.
    """, 
    'author': 'kene offiah',
    'website': 'https://www.procenix.com',
    'depends': ['stock', 'product'],
    'license': 'OPL-1',
    'price': 11.90,
    'currency': 'USD',
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
