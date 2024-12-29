from odoo import models, fields, api

class AuctionProduct(models.Model):
    _name = 'auction.product'
    _description = 'Producto'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    price = fields.Float(related='product_id.lst_price', string='Precio de Venta', store=True, readonly=False)
