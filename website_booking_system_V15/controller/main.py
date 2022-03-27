# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and  licensing details.

from odoo import http
from odoo.http import request
from datetime import date, timedelta
import calendar 
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo import fields, SUPERUSER_ID, tools, _

class WebsiteSaleInherit(WebsiteSale):
    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        """
        This route is called :
            - When changing quantity from the cart.
            - When adding a product from the wishlist.
            - When adding a product to cart on the same page (without redirection).
        """
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=1)
            else:
                return {}

        pcav = kw.get('product_custom_attribute_values')
        nvav = kw.get('no_variant_attribute_values')
        # temp_book_date = kw.get('book_date')
        # temp_date = temp_book_date.split("\n")
        # book_date = temp_date[0]+' '+temp_date[1]
        # temp_book_plan = kw.get('book_plan')
        # temp_plan = temp_book_plan.split(" ")
        # book_plan = temp_plan[0]
        # book_price = temp_plan[1].split("$ ")[1]

        book_slot_record_time = request.env['booking.slot'].sudo().search([('id', '=', kw.get('book_time'))])
        book_slot_record_plan = request.env['booking.slot'].sudo().search([('id', '=', kw.get('book_plan'))])

        value = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            book_time=book_slot_record_time.time_slot_id.combination,
            book_date=kw.get('book_date'),
            book_plan=book_slot_record_plan.plan_id.name,
            book_price=book_slot_record_plan.price,
            product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
            no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None
        )

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
            'website_sale_order': order,
        })
        return value

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

        data={"template_data":request.env['ir.ui.view']._render_template("ak_website_booking_system.pop_up_modal", extra_dict),

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

        data={"template_data_time":request.env['ir.ui.view']._render_template("ak_website_booking_system.pop_up_time_modal", extra_dict),  
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
                "template_data_plan":request.env['ir.ui.view']._render_template("ak_website_booking_system.pop_up_plan_modal", extra_dict),             
            }
        return data        





