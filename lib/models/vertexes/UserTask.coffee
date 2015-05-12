Vertex = require('../Vertex')

# User Task
# Maps to bpmn2:userTask
class UserTask extends Vertex
    Name: 'UserTask'
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
    ]


module.exports = UserTask
