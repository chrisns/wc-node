class GraphEntity
    strictMode: true
    defined_properties: {}

    getDefinition: ->
        throw Error 'Not implemented yet'

    format_string: (value) ->
        if typeof value isnt 'string'
            throw Error 'Wrong type'
        return value

    format_boolean: (value) ->
        if typeof value isnt 'boolean'
            throw Error 'Wrong type'
        return value

    format_integer: (value) ->
        if typeof value isnt 'number'
            throw Error 'Wrong type'
        return value

    format_short: (value) ->
        if typeof value isnt 'number' or value >= 32768 or value <= -32768
            throw Error 'Wrong type'
        return value

    format_long: (value) ->
        if typeof value isnt 'number'
            throw Error 'Wrong type'
        return value

    format_date: (value) ->
        throw Error 'Not implemented yet'

    format_double: (value) ->
        throw Error 'Not implemented yet'

    format_binary: (value) ->
        throw Error 'Not implemented yet'

    format_embedded: (value) ->
        throw Error 'Not implemented yet'

    format_embeddedlist: (value) ->
        throw Error 'Not implemented yet'

    format_embeddedset: (value) ->
        throw Error 'Not implemented yet'

    format_embeddedmap: (value) ->
        throw Error 'Not implemented yet'

    format_linked: (value) ->
        throw Error 'Not implemented yet'

    format_link: (value) ->
        throw Error 'Not implemented yet'

    format_linklist: (value) ->
        throw Error 'Not implemented yet'

    format_linkset: (value) ->
        throw Error 'Not implemented yet'

    format_linkmap: (value) ->
        throw Error 'Not implemented yet'

    format_byte: (value) ->
        throw Error 'Not implemented yet'

    set: (key, value) ->
        if not @defined_properties[key]? and @schema is true
            throw new Error 'Not allowed'
        if @defined_properties[key]?
            formatter = 'format_' + @defined_properties[key]

            this[key] = this[formatter](value)
        else
            this[key] = value

    validate: () ->
        if @strictMode is not true
            return true
        for key in Object.keys(@defined_properties)
            if this[key] is undefined
                throw Error 'Missing input'
#        throw Error 'Not implemented yet'
#    constructor: ->
#        defined_properties = @defined_properties
#        Object.keys(defined_properties).forEach (key) ->
#            console.log(defined_properties[key])
#            Object.defineProperties @prototype,
#                [key]:
#                    set: (name) -> [@firstName, @lastName] = name.split ' '


#    Object.defineProperties @prototype,
#        fullName:
##            get: -> "#{@firstName} #{@lastName}"
#            set: (name) -> [@firstName, @lastName] = name.split ' '

###
      if k not in self.defined_properties and k not in self.allowed:
            raise Exception("%s not an allowed property" % k)
        if k in self.defined_properties:
            formatter = "self.format_" + self.defined_properties[k]
            v = eval(formatter)(v)
        super(GraphObject, self).__setattr__(k, v)

###

module.exports = GraphEntity