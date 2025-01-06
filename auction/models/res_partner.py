from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    auction_won_count = fields.Integer(string="Subastas Ganadas", compute='_compute_auction_won_count')
    auction_won_ids = fields.One2many('auction.register', 'winner_id', string='Subastas Ganadas')

    @api.depends('auction_won_ids')
    def _compute_auction_won_count(self):
        for partner in self:
            partner.auction_won_count = len(partner.auction_won_ids)

    def action_auction_won(self):
        self.ensure_one()
        action = self.env.ref('auction.action_auction_won').read()[0]
        action['domain'] = [('winner_id', '=', self.id)]
        action['context'] = {'default_winner_id': self.id}
        return action

