from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AuctionWebsite(http.Controller):

    @http.route('/auctions', type='http', auth='public', website=True)
    def auctions(self, **kwargs):
        auctions = request.env['auction.register'].sudo().search([])
        return request.render('auction.auction_page', {
            'auctions': auctions,
        })

    @http.route('/auction/<model("auction.register"):auction>', type='http', auth='public', website=True)
    def auction_details(self, auction, **kwargs):
        return request.render('auction.auction_detail_page', {
            'auction': auction,
        })

    @http.route('/auction/bid/<model("auction.register"):auction>', type='http', auth='public', website=True)
    def auction_bid(self, auction, **kwargs):
        users = request.env['res.partner'].sudo().search([])
        return request.render('auction.auction_bid_page', {
            'auction': auction,
            'users': users,
        })

    @http.route('/submit_bid', type='json', auth='public', methods=['POST'])
    def submit_bid(self, auction_id, bid_amount, user_id):
        _logger.info(f'Received bid submission: auction_id={auction_id}, bid_amount={bid_amount}, user_id={user_id}')
        try:
            auction = request.env['auction.register'].sudo().browse(auction_id)
            if not auction:
                _logger.error('Auction not found.')
                return {'success': False, 'message': 'Subasta no encontrada.'}
        
            if bid_amount <= auction.current_price:
                _logger.error('Bid amount is not greater than the current price.')
                return {'success': False, 'message': 'El monto de la puja debe ser mayor al precio actual.'}
        
            request.env['auction.bid'].sudo().create({
                'user_id': user_id,
                'auction_id': auction.id,
                'amount': bid_amount,
            })
        
            auction.sudo().write({'current_price': bid_amount})

            _logger.info('Bid successfully submitted.')
            return {'success': True, 'message': 'Puja realizada con éxito.'}
        except Exception as e: 
            _logger.error(f'Error while submitting bid: {str(e)}') 
            return {'success': False, 'message': f'Error: {str(e)}'}
