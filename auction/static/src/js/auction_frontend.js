odoo.define('auction.auction_frontend', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.auctionFrontend = publicWidget.Widget.extend({
        selector: '.oe_structure',
        start: function () {
            console.log('Auction Frontend Loaded');
        },
    });

});
