from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AuctionRegister(models.Model):
    _name = 'auction.register'
    _description = 'Subasta'

    name = fields.Char('Nombre', required=True)
    product_id = fields.Many2one('product.product', 'Producto')
    start_date = fields.Date('Fecha de Inicio')
    end_date = fields.Date('Fecha de Cierre')
    sale_price = fields.Float('Precio Inicial', related='product_id.lst_price')
    current_price = fields.Float('Precio Actual', compute='_compute_current_price')
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en proceso', 'En proceso'),
        ('terminada', 'Terminada'),
        ('cancelada', 'Cancelada'),
    ], 'Estado', default='borrador')
    bid_ids = fields.One2many('auction.bid', 'auction_id', 'Licitaciones')
    winner_id = fields.Many2one('res.partner', 'Ganador', readonly=True)

    @api.depends('bid_ids')
    def _compute_current_price(self):
        for record in self:
            record.current_price = max(record.mapped('bid_ids.amount') or [record.current_price])
    
    def write(self, vals): 
        res = super(AuctionRegister, self).write(vals) 
        for record in self: 
            if 'state' in vals and vals['state'] == 'terminada':
                highest_bid = max(record.bid_ids, key=lambda bid: bid.amount, default=None) 
                if highest_bid: 
                    record.winner_id = highest_bid.user_id 
        return res 