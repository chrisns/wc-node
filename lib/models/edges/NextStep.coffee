Edge = require('../Edge')

# Relationship between steps
class NextStep extends Edge
    Name: 'NextStep'
    SuperClass: 'E'
    builtin: false
    schema: true
    defined_properties: [
        name: 'condition'
        type: 'string'
    ,
        name: 'id'
        type: 'string'
    ]


module.exports = NextStep