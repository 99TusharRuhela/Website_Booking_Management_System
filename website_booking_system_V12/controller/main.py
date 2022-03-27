# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and  licensing details.
import json
from odoo import http
from odoo.http import request
from datetime import date, timedelta
import calendar 
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import fields, SUPERUSER_ID, tools, _

class WebsiteSaleInherit(WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, line_id=None, add_qty=None, set_qty=None, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        book_slot_record_time = request.env['booking.slot'].sudo().search([('id', '=', kw.get('book_time'))])
        book_slot_record_plan = request.env['booking.slot'].sudo().search([('id', '=', kw.get('book_plan'))])    

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            book_time=book_slot_record_time.time_slot_id.combination,
            book_date=kw.get('book_date'),
            book_plan=book_slot_record_plan.plan_id.name,
            book_price=book_slot_record_plan.price,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")

class BookingReservation(http.Controller):

    @http.route('/get/popup/modal', csrf=False, type="json", methods=['POST'], auth="public", website=True)
    def get_popup_modal(self, book_product_id , *kw):
        product_record = request.env['product.template'].sudo().search([('id', '=', book_product_id)])
        product_vals_list = []
        today = date.today()
        delta = product_record.end_date - today
        for i in range(delta.days + 1):
            product_vals_dict = {}
            temp_btw_date = today + timedelta(days=i)
            btw_date = temp_btw_date.day
            btw_day = calendar.day_name[temp_btw_date.weekday()][0:3]
            btw_month = calendar.month_abbr[temp_btw_date.month]
            product_vals_dict['btw_date'] = btw_date
            product_vals_dict['btw_day'] = btw_day
            product_vals_dict['btw_month'] = btw_month
            product_vals_dict['full_date'] = temp_btw_date
            product_vals_list.append(product_vals_dict)

        extra_dict = {"product_record": product_record,
                      "data_dict_date": product_vals_list}

        data={"template_data":request.env['ir.ui.view'].render_template("ak_website_booking_system.pop_up_modal", extra_dict),

            }
        return data

    @http.route('/get/popup/modal/time', csrf=False, type="json", methods=['POST'], auth="public", website=True)
    def get_popup_modal_time(self, get_config_id, book_product_id , *kw):
        product_record = request.env['product.template'].sudo().search([('id', '=', book_product_id)])
        product_slot_list = []
        for line_config in product_record.config_time_slots_ids:
            if int(line_config.id) == int(get_config_id):
                for line_book in line_config.booking_slot_ids:
                    product_slot_dict ={}
                    product_slot_dict['time_slot'] = line_book.time_slot_id.combination
                    product_slot_dict['plan'] = line_book.plan_id.name
                    product_slot_dict['quantity'] = line_book.quantity
                    product_slot_dict['price'] = line_book.price
                    product_slot_dict['id'] = line_book.id
                    product_slot_dict['product_template_id'] = line_book.template_product_id.name
                    product_slot_list.append(product_slot_dict)                    


        temp = list({v['time_slot']:v for v in product_slot_list}.values())

        extra_dict = {"product_record": product_record,
                      "data_dict_product": temp,
                      }

        data={"template_data_time":request.env['ir.ui.view'].render_template("ak_website_booking_system.pop_up_time_modal", extra_dict),  
            }
        return data


    @http.route('/get/popup/modal/slot/time', csrf=False, type="json", methods=['POST'], auth="public", website=True)
    def get_popup_modal_slot_time(self, book_slot_time_id, product_template_id, *kw):
        book_slot_obj = request.env['booking.slot']
        booking_slot_record = book_slot_obj.sudo().search([('id', '=', book_slot_time_id)])
        temp = book_slot_obj.sudo().search([('booking_configure_id', '=', booking_slot_record.booking_configure_id.book_day),('template_product_id', '=', product_template_id)])
        product_slot_plan_list = []
        final_product_slot_plan_list = []

        for rec in temp:
            product_slot_plan_dict ={}
            product_slot_plan_dict['time_slot'] = rec.time_slot_id.combination
            product_slot_plan_dict['plan'] = rec.plan_id.name
            product_slot_plan_dict['quantity'] = rec.quantity
            product_slot_plan_dict['price'] = rec.price
            product_slot_plan_dict['id'] = rec.id
            product_slot_plan_list.append(product_slot_plan_dict)

        for line_list in product_slot_plan_list:
            if line_list['time_slot'] == booking_slot_record.time_slot_id.combination:
                final_product_slot_plan_list.append(line_list)


        extra_dict = {"booking_slot_record": booking_slot_record,
                      "data_dict_plan": final_product_slot_plan_list,
                      }

        data={
                "template_data_plan":request.env['ir.ui.view'].render_template("ak_website_booking_system.pop_up_plan_modal", extra_dict),             
            }
        return data        





