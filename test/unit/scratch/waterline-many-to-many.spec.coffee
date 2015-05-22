Promise = require 'bluebird'
setupWaterline = Promise.promisify require '../../../node_modules/sails-orientdb/example/raw/bootstrap'
connections =
  associations:
    adapter: 'sails-orientdb'
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    database: 'example-waterline-manyToMany'
    options:
      databaseType: 'graph'
      unsafeDrop: 'true'
      storage: 'memory'
collections =
  celebrity:
    migrate: 'drop'
    tableName: 'celebrityTable'
    identity: 'celebrity'
    connection: 'associations'
    attributes:
      name: 'string'
      people:
        collection: 'person'
        through: 'likes'
        via: 'celebrity'
  person:
    migrate: 'drop'
    tableName: 'personTable'
    identity: 'person'
    connection: 'associations'
    attributes:
      name: 'string'
      celebrities:
        collection: 'celebrity'
        through: 'likes'
        via: 'person'
  likes:
    migrate: 'drop'
    tableName: 'likesTable'
    identity: 'likes'
    connection: 'associations'
    attributes:
      since: 'date'
      person:
        model: 'person'
        columnName: 'person'
      celebrity:
        model: 'celebrity'
        columnName: 'celebrity'
setupWaterline({
  collections: collections
  connections: connections
})
.then (ontology) ->
  Promise.join(
    ontology.collections.celebrity.create({name: 'Megan Fox'}),
    ontology.collections.person.create({name: 'John Smith'}),
    (celebrity, person) ->
      ontology.collections.likes.create
        since: new Date()
        celebrity: celebrity.id
        person: person.id
      .then (edge) ->
        console.log edge
        ontology.collections.celebrity.find(celebrity.id).populate('people').then console.log
  )

.finally process.exit
