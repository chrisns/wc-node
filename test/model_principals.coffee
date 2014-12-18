chai = require('chai')
chaiAsPromised = require('chai-as-promised')
expect = chai.expect
winston = require('winston')
config = require('../config')
chai.use(chaiAsPromised)
chai.should()
randomId = require('../lib/randomid')
Oriento = require('oriento')
randomId = require('../lib/randomid')
server = Oriento()
Vertex = require('../lib/models/Vertex')
config = require('../config')

class TestGraphObject extends Vertex
    Name: 'TestGraphObject'
    SuperClass: 'V'
    builtin: false
    schema: true
    strictMode: true
    defined_properties: {
        name: 'string'
        id: 'string'
        fa: 'link'
    }



describe 'Model usage principals', ->
    server_config = config.orient_db_config
    server = Oriento(server_config)

    beforeEach ->
        @graphObject = new TestGraphObject
        @db_name = 'test_' + randomId()
        server.create
            name: @db_name,
            type: 'graph',
            storage: 'memory'
        .tap (database) =>
            @db = database

    afterEach ->
        server.drop
            name: @db_name



    it 'should be able to create itself', ->
        expect =>
            @graphObject.updateSchema(@db)
        .to.not.throw(Error)

    it 'should provide a valid definition', ->
        @graphObject.set('name', 'foo')
        @graphObject.set('id', 'bar')
        @graphObject.strictMode = false
        expect(@graphObject.getDefinition()).to.eql({
            '@class': 'TestGraphObject'
            'id': 'bar'
            'name': 'foo'
        })

    it 'Should throw error on unexpected input against schema', ->
        expect =>
            @graphObject.set('shouldfail', 'fail')
        .to.throw(Error)


    it 'Should not throw error on validation if not in strictMode', ->
        @graphObject.strictMode = false
        expect =>
            @graphObject.validate()
        .to.not.throw(Error)

    it 'Should throw error on validation if required fields are missing', ->
        expect =>
            @graphObject.validate()
        .to.throw(Error)

    it 'Should allow pass a correct boolean true value', ->
        expect =>
            @graphObject.format_boolean(true)
        .to.not.throw(Error)

    it 'Should allow pass a correct boolean false value', ->
        expect =>
            @graphObject.format_boolean(false)
        .to.not.throw(Error)

    it 'Should throw error on trying to pass a string as boolean', ->
        expect =>
            @graphObject.format_boolean('fail me')
        .to.throw(Error)

    it 'Should throw error on trying to pass an integer as boolean', ->
        expect =>
            @graphObject.format_boolean(12354)
        .to.throw(Error)

    it 'Should format an integer correctly', ->
        expect =>
            @graphObject.format_integer(12354)
        .to.not.throw(Error)

    it 'Should throw an error on bad integer', ->
        expect =>
            @graphObject.format_integer('1235')
        .to.throw(Error)

    it 'should format a short integer correctly', ->
        expect =>
            @graphObject.format_short(123)
        .to.not.throw(Error)

    it 'should thrown an error on a big short integer', ->
        expect =>
            @graphObject.format_short(12123354)
        .to.throw(Error)

    it 'should format a long integer correctly', ->
        expect =>
            @graphObject.format_long(1212335412123354)
        .to.not.throw(Error)

    it 'should throw an error on a bad long integer', ->
        expect =>
            @graphObject.format_long('1235')
        .to.throw(Error)

    it 'should format a date correctly', ->
        date = new Date()
        expect =>
            @graphObject.format_date(date)
        .to.not.throw(Error)

    it 'should throw an error on a bad date', ->
        expect =>
            @graphObject.format_date(1212335412123354)
        .to.throw(Error)

    it 'should format a string correctly', ->
        expect =>
            @graphObject.format_string('good string')
        .to.not.throw(Error)

    it 'should throw error on bad string', ->
        expect =>
            @graphObject.format_string(12345)
        .to.throw(Error)
