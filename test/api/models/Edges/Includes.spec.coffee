Model = require 'api/models/Edges/Includes'

describe 'The Includes Edge model', ->
  it 'should be an edge', ->
    expect Model.orientdbClass
    .to.eql 'E'

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .be.undefined
