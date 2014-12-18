Vertex = require('../Vertex')

# Form Field Value
# Maps to camunda:formField
class FormField extends Vertex
    Name: 'FormField'
    SuperClass: 'V'
    builtin: false
    defined_properties: {
        name: 'string'
        id: 'string'
        label: 'string'
        type: 'string'
        weight: 'short'
    }



module.exports = FormField
