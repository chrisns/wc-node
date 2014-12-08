Vertex = require('../Vertex')

# Form Field Value
#  Maps to camunda:value
class FormFieldValue extends Vertex
  Name: 'FormFieldValue'
  SuperClass: 'V'
  builtin: false
  defined_properties: {
    name: 'string'
    id: 'string'
  }


module.exports = FormFieldValue
