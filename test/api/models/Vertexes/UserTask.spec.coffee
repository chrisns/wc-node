Model = require 'api/models/Vertexes/UserTask'

describe 'The UserTask Vertex model', ->
  it 'should define the necessary attributes', ->
    expect Model.attributes
    .to.contain.keys 'name'
