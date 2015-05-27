module.exports =
  connection: 'testOrient'
  attributes:
    name: 'string'
    people:
      collection: 'person'
      through: 'likes'
      via: 'celebrity'
