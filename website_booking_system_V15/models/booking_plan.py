# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class BookingPlan(models.Model):
    _name = 'booking.plan'
    _description = 'Booking Plan'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")
    description = fields.Html(string="Description") 
