from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AuctionBid(models.Model):
    _name = 'auction.bid'
    _description = 'Licitaciones'

    user_id = fields.Many2one('res.partner', 'Usuario', required=True, default=lambda self: self.env.user)
    auction_id = fields.Many2one('auction.register', string='Subasta', required=True, ondelete='cascade')
    amount = fields.Float('Monto', required=True)
    date = fields.Datetime('Fecha', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if 'auction_id' in vals:
            auction = self.env['auction.register'].browse(vals['auction_id'])
            if auction.state != 'en proceso':
                raise ValidationError("Solo se pueden hacer pujas en subastas activas.")
            if vals['amount'] <= auction.sale_price or vals['amount'] <= auction.current_price:
                raise ValidationError("El monto de la puja debe ser mayor al precio inicial o precio actual de la subasta.")
        result = super(AuctionBid, self).create(vals)
        auction.write({'current_price' : vals['amount']})
        return result

    def write(self, vals):
        for record in self:
            if 'auction_id' in vals:
                auction_id = vals.get('auction_id', record.auction_id.id)
                auction = self.env['auction.register'].browse(auction_id)
                if auction.state != 'en proceso':
                    raise ValidationError("Solo se pueden hacer pujas en subastas activas.")
                if 'amount' in vals and (vals['amount'] <= auction.sale_price or vals['amount'] <= auction.current_price):
                    raise ValidationError("El monto de la puja debe ser mayor al precio inicial o precio actual de la subasta.")
        return super(AuctionBid, self).write(vals)
