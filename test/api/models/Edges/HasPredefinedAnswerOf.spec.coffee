Model = require 'api/models/Edges/HasPredefinedAnswerOf'

describe 'The HasPredefinedAnswerOf Edge model', ->
  it 'should be an edge', ->
    expect Model.orientdbClass
    .to.eql 'E'

  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.be.undefined
