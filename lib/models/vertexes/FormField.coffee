Vertex = require('../Vertex')

# Form Field Value
# Maps to camunda:formField
class FormField extends Vertex
    Name: 'FormField'
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
            name: 'label'
            type: 'string'
        ,
            name: 'weight'
            type: 'short'
        ,
            name: 'type'
            type: 'string'
    ]


module.exports = FormField
