{
    'name': 'QR Code Delivery Order',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Add QR codes with sales data to delivery orders',
    'description': """
This module adds QR codes containing customer sales data to delivery order templates.

Features:
- Generates QR codes with customer order information in CSV format
- Displays QR codes on printed delivery orders
- Includes customer details, order number, and delivery method

QR Code contains CSV data with:
- Customer Order Number
- Customer Name
- Customer Address/Location (State/Region)
- Customer Phone Number
- Customer Email Address
- Delivery/Shipping Method
    """,
    'author': 'kene offiah charles@procenix.com',
    'depends': ['stock', 'sale', 'delivery'],
    'license': 'OPL-1',
    'price': 13.90,
    'currency': 'USD',
    'external_dependencies': {
        'python': ['qrcode', 'PIL'],
    },
    'data': [
        'views/stock_picking_views.xml',
        'report/delivery_report_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}