express = require 'express'
router = express.Router()

# GET home page.
router.get '/', (req, res) ->
  res.hal
    data:
      currentlyProcessing: 14
      shippedToday: 20
    links:
      self: "/orders"
      next: "/orders?page=2"
      find:
        href: "/orders{?id}"
        templated: true
    embeds:
      orders: [
        data:
          total:    30.00
          currency: "USD"
          status:   "shipped"
        links:
          self:     "/orders/123"
          basket:   "/baskets/98712"
          customer: "/customers/7809"
        data:
          total:    20.00
          currency: "USD"
          status:   "processing"
        links:
          self:     "/orders/124"
          basket:   "/baskets/97213"
          customer: "/customers/12369"
      ]

module.exports = router
