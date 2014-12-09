randomId = require('../lib/randomid')
chai = require('chai')
expect = chai.expect


describe 'Random ID Generator', ->

    it 'Should be able to create an id with correct length', ->
        random_id = randomId()
        return expect(random_id).to.have.length.of(19)

    it 'Should be able to unique ids', ->
        random_id1 = randomId()
        random_id2 = randomId()
        return expect(random_id1).to.not.equal(random_id2)
