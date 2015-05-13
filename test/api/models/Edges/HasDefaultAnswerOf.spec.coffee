Model = require 'api/models/Edges/HasDefaultAnswerOf'

describe 'The HasDefaultAnswerOf Edge model', ->
  it 'should be an edge', ->
    expect Model.orientdbClass
    .to.eql 'E'

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.be.undefined
