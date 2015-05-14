Model = require __dirname.replace(__base + '/test/unit', 'api') + '/' + __file

describe 'The HasDefaultAnswerOf Edge model', ->
  it 'should be an edge', ->
    expect Model
    .to.be.a.model.and.to.be.an.edge

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.be.undefined
