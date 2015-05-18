Model = require __dirname.replace(__base + '/test/unit', 'api/') + '/' + __file

describe 'The Answered Edge model', ->
  it 'should be a vertex', ->
    expect Model
    .to.be.a.model.and.be.an.edge

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .be.undefined
