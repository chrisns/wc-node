module.exports =
  connection: 'testOrient'
  attributes:
    name: 'string'
    celebrities:
      dominant: true
      collection: 'celebrity'
      through: 'likes'
      via: 'person'
