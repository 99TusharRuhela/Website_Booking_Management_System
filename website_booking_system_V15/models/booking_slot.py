# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class BookingSlot(models.Model):
    _name = 'booking.slot'
    _description = 'Booking Slot'
    _rec_name = 'time_slot_id'

    time_slot_id = fields.Many2one('booking.time.slot', string="Time Slot", required=True)
    plan_id = fields.Many2one('booking.plan', string="Booking Plan", required=True)
    quantity = fields.Integer(string="Quantity")
    price = fields.Float(string="Price", required=True)
    template_product_id = fields.Many2one('product.template', string="Product Template Id", related="booking_configure_id.product_template_id")
    booking_configure_id = fields.Many2one('booking.config.time.slot', string="Booking Configure Time Slot Id")
