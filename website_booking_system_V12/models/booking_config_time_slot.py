# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class BookingConfigTimeSlot(models.Model):
    _name = 'booking.config.time.slot'
    _description = 'Booking Config Time Slot'
    _rec_name = 'book_day'

    book_day = fields.Selection([('Mon', 'Monday'), 
                                 ('Tue', 'Tuesday'), 
                                 ('Wed', 'Wednesday'), 
                                 ('Thu', 'Thursday'),
                                 ('Fri', 'Friday'),
                                 ('Sat', 'Saturday'),
                                 ('Sun', 'Sunday'),
                                 ], required=True)
    book_status = fields.Selection([('open', 'Open'),('close', 'Close')], required=True)
    product_template_id = fields.Many2one('product.template', string="Product Template Id")
    booking_slot_ids = fields.One2many('booking.slot', 'booking_configure_id', string="Booking Slot")
    