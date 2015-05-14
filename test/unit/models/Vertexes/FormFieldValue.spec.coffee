Model = require __dirname.replace(__base + '/test/unit', 'api/') + '/' + __file

describe 'The FormFieldValue Vertex model', ->
  it 'should be a vertex', ->
    expect Model
    .to.be.a.model.and.be.a.vertex

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.contain.keys 'name'
