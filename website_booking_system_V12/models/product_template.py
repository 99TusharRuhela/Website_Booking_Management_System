# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date

class Products(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    is_available_booking = fields.Boolean(string="Available for booking")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    booking_qty = fields.Integer(string="Max Booking Qty")
    config_time_slots_ids = fields.One2many('booking.config.time.slot', 'product_template_id', string="Config Day Slots")

    @api.onchange('is_available_booking')
    def _onchange_product_type(self):
        if self.is_available_booking:
            self.type = 'service'
        else:
            self.type = 'product'

    @api.model        
    def get_service_product(self, service_product_id):
        temp = service_product_id
        temp_product = self.search([('id', '=', temp.get('service_product_id'))])
        result = False
        if temp_product:
            if temp_product.is_available_booking:
                result = temp_product.is_available_booking
        return result

    @api.model    
    def get_seat_available(self, service_product_id):
        temp = service_product_id
        result = False
        temp_qty = 0
        temp_product = self.search([('id', '=', temp.get('service_product_id'))])
        book_slot_record_time = self.env['booking.slot'].sudo().search([('id', '=', temp.get('booking_time'))])
        book_slot_record_plan = self.env['booking.slot'].sudo().search([('id', '=', temp.get('booking_plan'))])
        record = self.env['sale.order.line'].search([('product_id', '=', temp.get('service_product_id')), ('booking_time_slot', '=', book_slot_record_time.time_slot_id.combination), ('booking_plan', '=', book_slot_record_plan.plan_id.name), ('booking_date', '=', temp.get('booking_date'))])
        temp_date = date.fromisoformat(temp.get('booking_date')).strftime("%a")
        temp_product_id = temp.get('service_product_id')

        temp_book_config = self.env['booking.config.time.slot'].search([
            ('book_day', '=', temp_date), 
            ('product_template_id', '=', temp_product_id)])        

        combine_booking_slot_record = self.env['booking.slot'].search([
            ('time_slot_id', '=', book_slot_record_time.time_slot_id.combination), 
            ('plan_id', '=', book_slot_record_plan.plan_id.name),
            ('booking_configure_id', '=', temp_book_config.id),
            ('template_product_id', '=', temp_product_id)])

        record = self.env['sale.order.line'].search([
            ('product_id', '=', temp.get('service_product_id')), 
            ('booking_time_slot', '=', book_slot_record_time.time_slot_id.combination), 
            ('booking_plan', '=', book_slot_record_plan.plan_id.name), 
            ('booking_date', '=', temp.get('booking_date'))])
            
        if temp_product and record:
            if temp_product.is_available_booking:
                for rec in record:
                    temp_qty += int(rec.product_uom_qty)
                total_book_qty = int(temp.get('qty_product')) + temp_qty
                if total_book_qty <= combine_booking_slot_record.quantity:
                    result = temp_product.is_available_booking
                else:
                    result = False
        else:
            result = True
        return result
