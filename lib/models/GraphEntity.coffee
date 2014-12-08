class GraphEntity
    strictMode: true
    defined_properties: {}

    format_boolean: (value) ->
        if value not instanceof bool
            throw Error 'Wrong type'
        return value

    format_integer: (value) ->
        if value not instanceof int
            throw Error 'Wrong type'
        return value

    format_short: (value) ->
        if value not instanceof int or value >= 32768 or value <= -32768
            throw Error 'Wrong type'
        return value

    format_long: (value) ->
        if value not instanceof int
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

    get: (key) ->
        throw Error 'Not implemented yet'

    set: (key, value) ->
        throw Error 'Not implemented yet'

    validate: ->
        throw Error 'Not implemented yet'
###
      if k not in self.defined_properties and k not in self.allowed:
            raise Exception("%s not an allowed property" % k)
        if k in self.defined_properties:
            formatter = "self.format_" + self.defined_properties[k]
            v = eval(formatter)(v)
        super(GraphObject, self).__setattr__(k, v)

 def validate(self):
        # assert all fields have been defined
        if self.strictMode is True:
            for prop in self.defined_properties.keys():
                assert hasattr(self, prop)
###

module.exports = GraphEntity