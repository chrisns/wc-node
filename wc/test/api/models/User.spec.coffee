chai = require 'chai'
chaiAsPromised = require 'chai-as-promised'
expect = chai.expect
chai.use chaiAsPromised
chai.should()

User = require('../../../api/models/Vertexes/User')

assert = require 'assert'
describe 'The User Model', ->
  describe 'before the user is created', ->
    it 'should hash the password', ->
      User.beforeCreate {password: 'password'}, (err, user) ->
        expect(user.password).to.not.equal 'password'
