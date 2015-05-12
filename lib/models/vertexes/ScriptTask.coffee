Vertex = require('../Vertex')

# Workflow ScriptTask Node
# Maps to bpmn2:ScriptTask
class ScriptTask extends Vertex
    Name: 'ScriptTask'
    SuperClass: 'V'
    builtin: false
    schema: true
    defined_properties: [
        name: 'name'
        type: 'string'
    ,
        name: 'id'
        type: 'string'
    ,
        name: 'script'
        type: 'string'
    ,
    ]


module.exports = ScriptTask
