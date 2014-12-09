Vertex = require('../Vertex')

# Workflow ScriptTask Node
# Maps to bpmn2:ScriptTask
class ScriptTask extends Vertex
    Name: 'ScriptTask'
    SuperClass: 'V'
    builtin: false
    defined_properties: {
        name: 'string'
        id: 'string'
        script: 'string'
    }



module.exports = ScriptTask
