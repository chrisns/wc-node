Vertex = require('../Vertex')

# Workflow Start Node
# Maps to bpmn2:process
class Workflow extends Vertex
    Name: 'Workflow'
    SuperClass: 'V'
    builtin: false
    defined_properties: {
        id: 'string'
    }

module.exports = Workflow