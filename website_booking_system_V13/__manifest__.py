# -*- coding: utf-8 -*-
{
    'name': "Website Booking System",
    'summary': 'Website Booking System',
    'description': """
        Website Booking System
    """,
    'author': "Akili Systems Pvt Ltd.",
    'website': "http://www.akilisystems.in",
    'category': 'Services',
    'version': '1.0',
    'depends': ['website','web','product','sale','website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/booking_plan_view.xml',
        'views/booking_time_slot_view.xml',
        'views/booking_config_time_slot_view.xml',
        'views/booking_slot_view.xml',
    ],
}
