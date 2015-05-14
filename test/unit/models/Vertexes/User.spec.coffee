Model = require __dirname.replace(__base + '/test/unit', 'api/') + '/' + __file

describe 'The User Model', ->
  it 'should be a vertex', ->
    expect Model
    .to.be.a.model.and.be.a.vertex

  describe 'before the user is created', ->
    it 'should hash the password', ->
      Model.beforeCreate {password: 'password'}, (err, model) ->
        expect(model.password).to.not.equal 'password'
