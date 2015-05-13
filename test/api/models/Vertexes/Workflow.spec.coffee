Model = require 'api/models/Vertexes/Workflow'

describe 'The Workflow Vertex model', ->
  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.be.undefined
