# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class BookingTimeSlot(models.Model):
    _name = 'booking.time.slot'
    _description = 'Booking Time Slot'
    _rec_name = 'combination'

    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('start_time', 'end_time')
    def _compute_fields_combination(self):
        for rec in self:
            rec.combination = str(rec.start_time) + ' - ' + str(rec.end_time)
