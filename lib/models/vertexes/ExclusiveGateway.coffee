Vertex = require('../Vertex')

# Exclusive Gateway
# Maps to bpmn2:exclusiveGateway
class ExclusiveGateway extends Vertex
  Name: 'ExclusiveGateway'
  SuperClass: 'V'
  builtin: false
  defined_properties: {
    name: 'string'
    id: 'string'
  }


module.exports = ExclusiveGateway