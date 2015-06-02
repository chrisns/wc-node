module.exports =
  connection: 'testOrient'
  attributes:
    name: 'string'
    friends:
      dominant: true
      collection: 'boy'
      through: 'friends'
      via: 'boyb'
    friends_with:
      dominant: true
      collection: 'boy'
      through: 'friends'
      via: 'boyb'
