Model = require 'api/models/Edges/NextStep'

describe 'The NextStep Edge model', ->
  it 'should be an edge', ->
    expect Model.orientdbClass
    .to.eql 'E'

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.have.keys('condition')
