odoo.define('ak_website_booking_system.website_sale_utils_inherit', function (require) {
"use strict";

var rpc = require('web.rpc');
const websiteSaleTracking = require('website_sale.tracking');
require('website_sale.website_sale');
var core = require('web.core');
var config = require('web.config');
var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');
var wSaleUtils = require('website_sale.utils');
const wUtils = require('website.utils');
require("web.zoomodoo");
    
    publicWidget.registry.WebsiteSale.include({
        _submitForm: function () {
            let params = this.rootProduct;
            params.add_qty = params.quantity;

            params.product_custom_attribute_values = JSON.stringify(params.product_custom_attribute_values);
            params.no_variant_attribute_values = JSON.stringify(params.no_variant_attribute_values);
            
            var temp_result
            var self = this
            rpc.query({
                model: 'product.template',
                method: 'get_service_product',
                args: [{'service_product_id':params['product_id']}],
            }).then(function (result) { 
                    temp_result = result
                    if (temp_result === true) {
                        var book_date = document.getElementsByClassName("style-active-day")[0].children[3].value;
                        var book_time = document.getElementsByClassName("style-active-time")[0].children[1].value;
                        var book_plan = document.getElementsByClassName("style-active-plan")[0].children[3].value;
                        var qty_product = document.getElementsByClassName("qtyProduct")[0].value;

                        rpc.query({
                            model: 'product.template',
                            method: 'get_seat_available',
                            args: [{
                                    'service_product_id':params['product_id'],
                                    'booking_date':book_date,
                                    'booking_time':book_time,
                                    'booking_plan':book_plan,
                                    'qty_product':qty_product,
                                }],
                        }).then(function (result) {
                            if (result === true) {
                                params['book_date'] = book_date
                                params['book_time'] = book_time
                                params['book_plan'] = book_plan
                                if (self.isBuyNow) {
                                    params.express = true;
                                }
                               
                                return wUtils.sendRequest('/shop/cart/update', params);
                            }
                            else {
                                alert("Seat Full")
                                window.location.reload()
                            }
                        })   
                    }
                    else {
                        if (self.isBuyNow) {
                            params.express = true;
                        }
                       
                        return wUtils.sendRequest('/shop/cart/update', params);
                    }
                });         
        },
    });
});