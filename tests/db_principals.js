/*global describe, beforeEach, afterEach, it */
var chai = require("chai");
var chaiAsPromised = require("chai-as-promised");
var expect = chai.expect;
var Oriento = require("oriento");
var winston = require('winston');
var randomId = require('../lib/randomid');
var server = Oriento();
var config = require('../config');
chai.use(chaiAsPromised);
chai.should();

describe('Database usage principals', function () {
    var server_config = config.orient_db_config;
    var server = Oriento(server_config);
    var db_name;
    var db;

    // create database
    beforeEach(function () {
        db_name = "test_" + randomId();
        return server.create({
            name: db_name,
            type: 'graph',
            storage: 'memory'
        }).then(function (database) {
            db = database;
            winston.debug("created " + db.name, db);
        });
    });

    // drop the database
    afterEach(function () {
        return server.drop({
            name: db_name
        }).then(function () {
            winston.debug("dropped " + db_name);
            db = {};
        });
    });

    it('Database should exist', function () {
        var exists = server.exists(db_name);
        return expect(exists).eventually.to.be.true;
    });

    it('Should be able to add a vertex', function () {
        var vertex = db.vertex.create({
            '@class': 'V',
            key: 'value',
            foo: 'bar'
        });
        return expect(vertex).eventually.to.have.deep.property('@rid');
    });

    it('Should be able to run a create transaction', function() {
        var transaction = db.begin()
            .create({'@class': 'V', name: 'me'})
            .create({'@class': 'V', name: 'wat?'})
            .commit();
        return expect(transaction).eventually.to.have.deep.property('created').length(2);
    })
});
