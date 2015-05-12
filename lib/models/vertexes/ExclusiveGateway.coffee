Vertex = require('../Vertex')

# Exclusive Gateway
# Maps to bpmn2:exclusiveGateway
class ExclusiveGateway extends Vertex
    Name: 'ExclusiveGateway'
    SuperClass: 'V'
    builtin: false
    schema: true
    defined_properties: [
        name: 'name'
        type: 'string'
    ,
        name: 'id'
        type: 'string'
    ]


module.exports = ExclusiveGateway