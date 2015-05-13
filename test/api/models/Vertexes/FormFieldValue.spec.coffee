Model = require 'api/models/Vertexes/FormFieldValue'

describe 'The FormFieldValue Vertex model', ->
  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.contain.keys 'name'
