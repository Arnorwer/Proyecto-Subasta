from odoo import http
from odoo.http import request

class Main(http.Controller):

    @http.route('/sign_in', type='http', auth="public", website=True)
    def sign_in(self, **kw):

        return request.render(
            'auction.sign_in',
        )