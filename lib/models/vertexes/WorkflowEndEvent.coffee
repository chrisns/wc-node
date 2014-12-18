Vertex = require('../Vertex')

# Workflow End Node
# Maps to bpmn2:process
class WorkflowEndEvent extends Vertex
    Name: 'WorkflowEndEvent'
    SuperClass: 'V'
    builtin: false
    defined_properties: {
        id: 'string'
    }


module.exports = WorkflowEndEvent