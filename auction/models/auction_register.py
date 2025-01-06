from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AuctionRegister(models.Model):
    _name = 'auction.register'
    _description = 'Subasta'

    name = fields.Char('Nombre', required=True)
    product_id = fields.Many2one('product.product', 'Producto')
    start_date = fields.Date('Fecha de Inicio')
    end_date = fields.Date('Fecha de Cierre')
    sale_price = fields.Float(related='product_id.lst_price', string='Precio Inicial', store=True, readonly=False)
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
            record.current_price = max(record.mapped('bid_ids.amount') or [record.sale_price])
    
    def write(self, vals): 
        res = super(AuctionRegister, self).write(vals) 
        for record in self: 
            if 'state' in vals and vals['state'] == 'terminada':
                highest_bid = max(record.bid_ids, key=lambda bid: bid.amount, default=None) 
                if highest_bid: 
                    record.winner_id = highest_bid.user_id 
        return res 
    
    @api.model 
    def _cron_close_expired_auctions(self): 
        _logger.info('Running cron job to close expired auctions.') 
        expired_auctions = self.search([('end_date', '<', fields.Datetime.now()), ('state', '=', 'en proceso')]) 
        for auction in expired_auctions: 
            auction.write({'state': 'terminada'}) 
            _logger.info(f'Auction {auction.name} terminada.')