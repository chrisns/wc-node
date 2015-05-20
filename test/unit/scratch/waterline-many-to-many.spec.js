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

var setupWaterline = require('../raw/bootstrap');

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
  venue: {
    tableName: 'venueTable',
    identity: 'venue',
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
        through: 'venue',
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
        through: 'venue',
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

  var team1, stadium1;

  ontology.collections.team.create({seats: 1234})
    .then(function (team) {
      team1 = team;

      return ontology.collections.stadium.create([{name: 'fooanswer1'}, {name: 'fooanswer2'}]);
    })
    .then(function (stadiums) {
      answer1 = stadiums[0];
      team1.stadiums.add(stadiums[0]);
      team1.stadiums.add(stadiums[1]);

      return team1.save();
    })
    .then(function (res) {
      //  return ontology.collections.team.findOne(team1.id).populate('stadium');
      //})
      //.then(function (populatedQuestion) {
      //  console.log('Question', populatedQuestion.question, 'has the following answers:', populatedQuestion.answers, '\n');
      //
      //  return ontology.collections.answer.findOne(answer1.id)
      //    .populate('questions');
      //})
      //.then(function (populatedAnswer) {
      //  console.log('Answer', populatedAnswer.answer, 'has the following questions:', populatedAnswer.questions, '\n');
      //  console.log('All done, have a nice day!\n');
      process.exit(0);
    });

})
;
