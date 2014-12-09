Vertex = require('../Vertex')

# User Task
# Maps to bpmn2:userTask
class UserTask extends Vertex
    Name: 'UserTask'
    SuperClass: 'V'
    builtin: false
    defined_properties: {
        name: 'string'
        id: 'string'
    }



module.exports = UserTask
