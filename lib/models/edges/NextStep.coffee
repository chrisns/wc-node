Edge = require('../Edge')

# Relationship between steps
class NextStep extends Edge
    Name: 'NextStep'
    SuperClass: 'E'
    builtin: false
    defined_properties: {
        condition: 'string'
    }



module.exports = NextStep