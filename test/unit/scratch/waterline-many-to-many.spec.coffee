setupWaterline = require '../../../node_modules/sails-orientdb/example/raw/bootstrap'
connections =
  associations:
    adapter: 'sails-orientdb'
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    database: 'example-waterline-manyToMany'
    options:
      storage: 'memory'
collections =
  connex:
    tableName: 'connexTable'
    identity: 'connex'
    connection: 'associations'
    orientdbClass: 'myclass'
    attributes:
      seats: 'integer'
      friend:
        columnName: '@in',
        type: 'string',
        foreignKey: true,
        references: 'friend',
        on: 'id',
        onKey: 'id',
        via: 'followee'
      followee:
        columnName: '@out',
        type: 'string',
        foreignKey: true,
        references: 'friend',
        on: 'id',
        onKey: 'id',
        via: 'friend'
  person:
    tableName: 'personTable'
    identity: 'person'
    connection: 'associations'
#    attributes:
#      name: 'string'
#      stadiums:
#        collection: 'Stadium'
#        through: 'connex'
#        via: 'team'
#        dominant: true
setupWaterline {
  collections: collections
  connections: connections
}, (err, ontology) ->
  if err
    throw err
  console.log '\nWaterline initialized\n'
  #  team1 = undefined
  ontology.collections.person.create [{name: "bob"}, {name: "jane"}]
  .then (people) ->
    ontology.collections.connex.create {seats: 12, friend: people[0], followee: people[1]}
  .done ->
    process.exit 0
#  ontology.collections.team.create(team: 'team1').then((team) ->
#    team1 = team
#    ontology.collections.stadium.create name: 'fooanswer1'
#  ).then((stadium) ->
#    team1.stadiums.add stadium
#    team1.save()
#  ).done ->
#    process.exit 0
#    return
#  return
