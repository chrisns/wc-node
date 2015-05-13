Model = require 'api/models/Vertexes/FormField'

describe 'The FormField Vertex model', ->
  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.contain.keys 'name', 'label', 'weight', 'type'
