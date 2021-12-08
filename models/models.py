# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class SaleLines(models.Model):
    _name = 'sale.lines'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    unit_of_measure = fields.Char(required=True)
    price = fields.Float(related='product_id.list_price')
    quantity = fields.Float(required=True)
    subtotal = fields.Float(compute='_calculate_line_subtotal', store=True)
    order_id = fields.Many2one('sales')

    @api.depends('price', 'quantity')
    def _calculate_line_subtotal(self):
        for line in self:
            line_subtotal = line.price * line.quantity
            line.update({'subtotal': line_subtotal})


    _sql_constraints = [
        (
            'check_quantity_greater_than_zero',
            'CHECK(quantity > 0.0)',
            "The quantity cannot be less than or equal zero.",
        ),
    ]


class SaleOrders(models.Model):
    _name = 'sales'
    _rec_name = 'id'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    line_id = fields.One2many('sale.lines', 'order_id', string='Lines')
    sum_of_subtotal = fields.Float(compute='_calc_lines_subtotal', store=True)
    discount_amount = fields.Float()
    discount_percentage = fields.Float('Percentage(%)')
    net_total = fields.Float('total', compute='_compute_order_net_total', store=True)
    order_state = fields.Selection([('new', 'New'), ('confirmed', 'Confirmed')],
                             string="Status", readonly=True, default='new')

    _sql_constraints = [
        (
            'check_discount_amount_non_negative',
            'CHECK(discount_amount >= 0.0)',
            "Discount Amount cannot be less than zero.",
        ),
        (
            'check_discount_percentage_non_negative',
            'CHECK(discount_percentage >= 0.0 and discount_percentage <= 100)',
            "Discount Percentage must be between 0 and 100 ..",
        ),
    ]


    @api.depends('line_id')
    def _calc_lines_subtotal(self):
        total = 0
        for order in self:
            for line in order.line_id:
                total += line.subtotal
        self.sum_of_subtotal = total


    @api.depends('discount_amount')
    def _compute_order_net_total(self):
        self.net_total = self.sum_of_subtotal - self.discount_amount


    @api.onchange('discount_amount', 'sum_of_subtotal')
    def _calc_discount_percentage(self):
        if self.discount_amount > 0:
            self.discount_percentage = (self.discount_amount / self.sum_of_subtotal) * 100

    @api.onchange('discount_percentage', 'sum_of_subtotal')
    def _calc_discount_amount(self):
        self.discount_amount = (self.discount_percentage * self.sum_of_subtotal) / 100


    def confirm_sale_order(self):
        self.order_state = 'confirmed'


    def create_invoice(self):
        invoice_lines = []
        for order in self:
            for line in order.line_id:
                invoice_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price,
                }))
        print("Invoice List : ", invoice_lines)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': date.today(),
            'date': date.today(),
            'invoice_line_ids': invoice_lines,
        })

        return invoice
