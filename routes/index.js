var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
  //res.json({ title: 'Express' });
  res.hal({
    data: {
      currentlyProcessing: 14,
      shippedToday: 20,
    },
    links: {
      self: "/orders",
      next: "/orders?page=2",
      find: { href: "/orders{?id}", templated: true }
    },
    embeds: {
      "orders": [
        {
          data: {
            total:    30.00,
            currency: "USD",
            status:   "shipped"
          },
          links: {
            self:     "/orders/123",
            basket:   "/baskets/98712",
            customer: "/customers/7809"
          }
        },
        {
          data: {
            total:    20.00,
            currency: "USD",
            status:   "processing"
          },
          links: {
            self:     "/orders/124",
            basket:   "/baskets/97213",
            customer: "/customers/12369"
          }
        }
      ]
    }
  });
  //res.render('index', { title: 'Express' });
});

module.exports = router;
