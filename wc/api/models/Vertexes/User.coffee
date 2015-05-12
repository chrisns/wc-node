Waterline = require 'waterline'

module.exports Waterline.Collection.extend
  attributes:
    username:
      type: 'string'
      required: true
      unique: true
    password:
      type: 'string'
      required: true

  beforeCreate: (user, cb) ->
    user.password = "fooooo"
    cb null, user
