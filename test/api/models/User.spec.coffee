User = require '../../../api/models/Vertexes/User'

describe 'The User Model', ->
  describe 'before the user is created', ->
    it 'should hash the password', ->
      User.beforeCreate {password: 'password'}, (err, user) ->
        expect(user.password).to.not.equal 'password'
