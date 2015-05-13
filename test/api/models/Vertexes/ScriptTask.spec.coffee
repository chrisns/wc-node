Model = require 'api/models/Vertexes/ScriptTask'

describe 'The ScriptTask Vertex model', ->
  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.contain.keys 'name', 'script'
