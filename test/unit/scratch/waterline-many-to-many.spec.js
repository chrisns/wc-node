/**
 * Based on http://stackoverflow.com/questions/28985075/sails-orientdb-bi-directional-edge
 * Associations docs at https://github.com/balderdashy/waterline-docs/blob/master/associations.md
 * More info at https://github.com/balderdashy/waterline
 */

//////////////////////////////////////////////////////////////////////////////
// Example on how to run:
// mkdir manyToMany
// cd manyToMany
// npm install waterline
// npm install sails-orientdb
// node node_modules/sails-orientdb/example/associations/many-to-many.js
//////////////////////////////////////////////////////////////////////////////

var setupWaterline = require('../../../node_modules/sails-orientdb/example/raw/bootstrap');

var connections = {
  associations: {
    adapter: 'sails-orientdb',
    host: 'localhost',
    port: 2424,
    user: 'root',
    password: 'root',
    database: 'example-waterline-manyToMany',
    options: {
      storage: 'memory'
    }
  }
};

var collections = {
  connex: {
    tableName: 'connexTable',
    identity: 'connex',
    connection: 'associations',

    attributes: {
      seats: 'integer',
      teamRef: {
        columnName: 'teamRef',
        type: 'string',
        foreignKey: true,
        references: 'team',
        on: 'id',
        onKey: 'id',
        via: 'stadiumRef'
      },
      stadiumRef: {
        columnName: 'stadiumRef',
        type: 'string',
        foreignKey: true,
        references: 'stadium',
        on: 'id',
        onKey: 'id',
        via: 'teamRef'
      }
    }
  },
  team: {
    tableName: 'teamTable',
    identity: 'team',
    connection: 'associations',

    attributes: {
      name: 'string',
      mascot: 'string',
      stadiums: {
        collection: 'Stadium',
        through: 'connex',
        via: 'team',
        dominant: true
      }

    }
  },
  stadium: {
    tableName: 'stadiumTable',
    identity: 'stadium',
    connection: 'associations',

    attributes: {
      name: 'string',
      teams: {
        collection: 'Team',
        through: 'connex',
        via: 'stadium'
      }
    }
  }
};

setupWaterline({
  collections: collections,
  connections: connections
}, function waterlineReady(err, ontology) {
  if (err) throw err;

  console.log('\nWaterline initialized\n');

  var team1;

  ontology.collections.team.create({team: 'team1'})
    .then(function (team) {
      team1 = team;

      return ontology.collections.stadium.create({name: 'fooanswer1'});
    })
    .then(function (stadium) {

      team1.stadiums.add(stadium);
      return team1.save();
    })
    .done(function () {
      process.exit(0);
    });

});
