chai = require("chai");
chaiAsPromised = require("chai-as-promised");
expect = chai.expect;
winston = require('winston');
config = require('../config');
chai.use(chaiAsPromised);
chai.should();

GraphEntity = require('../lib/models/GraphEntity')

class TestGraphObject extends GraphEntity
    name: 'Workflow'
    builtin: false
    schema: true
    strictMode: false
    defined_properties: {
        name: 'string'
        id: 'string'
        fa: 'link'
    }



describe 'Model usage principals', ->
    beforeEach ->
        @graphObject = new TestGraphObject

    it 'Should throw error on unexpected input against schema', ->
        graphObject = @graphObject
        expect ->
            graphObject.set('shouldfail', 'fail')
        .to.throw(Error)

    it 'Should throw error on validation if required fields are missing', ->
        expect(@graphObject.validate).to.throw(Error)

    it 'Should allow pass a correct boolean true value', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_boolean(true)
        .to.not.throw(Error)

    it 'Should allow pass a correct boolean false value', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_boolean(false)
        .to.not.throw(Error)

    it 'Should throw error on trying to pass a string as boolean', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_boolean('failme')
        .to.throw(Error)

    it 'Should throw error on trying to pass an integer as boolean', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_boolean(12354)
        .to.throw(Error)


    it 'Should format an integer correctly', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_integer(12354)
        .to.not.throw(Error)

    it 'Should throw an error on bad integer', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_integer("1235")
        .to.throw(Error)

    it 'should format a short integer correctly', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_short(123)
        .to.not.throw(Error)

    it 'should thrown an error on a big short integer', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_short(12123354)
        .to.throw(Error)

    it 'should format a long integer correctly', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_long(1212335412123354)
        .to.not.throw(Error)

    it 'should throw an error on a bad long integer', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_long("1235")
        .to.throw(Error)

    it 'should format a date correctly'

    it 'should throw an error on a bad date'

    it 'should format a string correctly', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_string("abcdefg")
        .to.not.throw(Error)

    it 'should throw error on bad string', ->
        graphObject = @graphObject
        expect ->
            graphObject.format_string(12345)
        .to.throw(Error)
###
    def test_format_date_good(self):
        good_date = datetime(2014, 11, 17, 06, 00, 00)
        self.assertEqual(self.o.format_date(good_date), "DATE('ISO', '2014-11-17 06:00:00')")
###