odoo.define('auction.auction_bid', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.auctionBid = publicWidget.Widget.extend({
        selector: '.auction-bid-page',
        events: {
            'submit #bid-form': '_onSubmitBid',
        },

        _onSubmitBid: function (event) {
            event.preventDefault();
            var bidAmount = this.$('#bid-amount').val();
            var userId = this.$('#user-id').val();
            var productId = this.$('#auction-product-details').data('product-id');
            if (!bidAmount || bidAmount <= 0) {
                alert('Por favor, ingrese un monto válido.');
                return;
            }
            ajax.jsonRpc('/submit_bid', 'call', {
                auction_id: productId,
                bid_amount: parseFloat(bidAmount),
                user_id: parseInt(userId),
            }).then(function (data) {
                if (data.success) {
                    alert('Puja realizada exitosamente.');
                } else {
                    alert('Error: ' + data.message);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert('Error en la solicitud: ' + textStatus + ' ' + errorThrown);
            });
        },
    });

});


