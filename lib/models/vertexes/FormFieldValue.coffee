Vertex = require('../Vertex')

# Form Field Value
#  Maps to camunda:value
class FormFieldValue extends Vertex
    Name: 'FormFieldValue'
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


module.exports = FormFieldValue
