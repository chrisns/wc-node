chai = require("chai");
chaiAsPromised = require("chai-as-promised");
expect = chai.expect;
Promise = require("bluebird");
Oriento = require("oriento");
winston = require('winston');
randomId = require('../lib/randomid');
server = Oriento();
config = require('../config');
chai.use(chaiAsPromised);
chai.should();

describe 'Database usage principals', ->
    server_config = config.orient_db_config
    server = Oriento(server_config)

    beforeEach ->
        @db_name = "test_" + randomId()
        return server.create({
            name: @db_name,
            type: 'graph',
            storage: 'memory'})
        .then (database) =>
            @db = database

    afterEach ->
        server.drop({
            name: @db_name
        })
        .then =>
            @db = {}

    it 'Database should exist', ->
        exists = server.exists(@db_name)
        return expect(exists).eventually.to.be.true

    it 'Should be able to add a vertex', ->
        vertex = @db.vertex.create({
            '@class': 'V'
            key: 'value'
            foo: 'bar'
        })
        return expect(vertex).eventually.to.have.deep.property('@rid')

    it 'Should be able to run a create transaction', ->
        transaction = @db.begin()
        .create({'@class': 'V', name: 'me'})
        .create({'@class': 'V', name: 'wat?'})
        .commit()
        return expect(transaction).eventually.to.have.deep.property('created').length(2)

    it 'Should be able to create a class with properties', ->
        myClassDefinition = {
            name: 'MyNewClass',
            superClass: 'V',
            properties: [
                {
                    name: 'AStringProperty',
                    type: 'String'
                },
                {
                    name: 'AnotherStringProperty',
                    type: 'String'
                }
            ]
        }
        createClassFromDefinition = (classDefinition) =>
            return @db.class.create(classDefinition.name, 'V')
            .tap (dbClass) ->
                propertyCreationPromises = classDefinition.properties.map(dbClass.property.create)
                return Promise.settle(propertyCreationPromises)

        newClass = createClassFromDefinition(myClassDefinition)
        return expect(newClass).eventually.to.have.deep.property('properties').length(2)
