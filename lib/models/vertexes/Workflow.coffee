Vertex = require('../Vertex')

# Workflow Start Node
# Maps to bpmn2:process
class Workflow extends Vertex
    Name: 'Workflow'
    SuperClass: 'V'
    builtin: false
    schema: true
    defined_properties: [
        name: 'id'
        type: 'string'
    ]

module.exports = Workflow