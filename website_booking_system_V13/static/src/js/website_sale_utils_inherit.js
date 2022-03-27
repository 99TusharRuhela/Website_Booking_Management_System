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
            var $productCustomVariantValues = $('<input>', {
                name: 'product_custom_attribute_values',
                type: "hidden",
                value: JSON.stringify(this.rootProduct.product_custom_attribute_values)
            });
            this.$form.append($productCustomVariantValues);

            var $productNoVariantAttributeValues = $('<input>', {
                name: 'no_variant_attribute_values',
                type: "hidden",
                value: JSON.stringify(this.rootProduct.no_variant_attribute_values)
            });
            this.$form.append($productNoVariantAttributeValues);

            if (this.isBuyNow) {
                this.$form.append($('<input>', {name: 'express', type: "hidden", value: true}));
            }

            var temp_result
            var self = this
            rpc.query({
                model: 'product.template',
                method: 'get_service_product',
                args: [{'service_product_id':self.rootProduct.product_id}],
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
                                    'service_product_id':self.rootProduct.product_id,
                                    'booking_date':book_date,
                                    'booking_time':book_time,
                                    'booking_plan':book_plan,
                                    'qty_product':qty_product,
                                }],
                        }).then(function (result) {
                            if (result === true) {
                                self.rootProduct.book_date = book_date
                                self.rootProduct.book_time = book_time
                                self.rootProduct.book_plan = book_plan
                                var $book_date = $('<input>', {
                                    name: 'book_date',
                                    type: "hidden",
                                    value: self.rootProduct.book_date
                                });
                                self.$form.append($book_date);

                                var $book_time = $('<input>', {
                                    name: 'book_time',
                                    type: "hidden",
                                    value: self.rootProduct.book_time
                                });
                                self.$form.append($book_time);

                                var $book_plan = $('<input>', {
                                    name: 'book_plan',
                                    type: "hidden",
                                    value: self.rootProduct.book_plan
                                });
                                self.$form.append($book_plan);
                                
                                self.$form.trigger('submit', [true]);
                                return new Promise(function () {});
                            }
                            else {
                                alert("Seat Full")
                                window.location.reload()
                            }
                        })   
                    }
                    else {
                        self.$form.trigger('submit', [true]);
                        return new Promise(function () {});
                    }
                });           
        },

    });
});