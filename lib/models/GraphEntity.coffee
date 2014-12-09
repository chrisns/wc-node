_ = require('lodash')
Promise = require('bluebird')

class GraphEntity
    strictMode: true
    defined_properties: {}
    properties: {}

    updateSchema: (db) ->
        return db.class.create(@name, @superClass)
        .catch =>
            return db.class.get(@name)
        .then (dbClass) =>
            propertyCreationPromises = _.map(@defined_properties, dbClass.property.create)
            return Promise.settle(propertyCreationPromises)

    getDefinition: ->
        @validate()
        inbuilt_properties =
            '@class': @name
        return _.extend(inbuilt_properties, @properties)

    set: (key, value) ->
        if not @defined_properties[key]? and @schema is true
            throw new Error('Not allowed')
        if @defined_properties[key]?
            formatter = 'format_' + @defined_properties[key]
            @properties[key] = this[formatter](value)
        else
            @properties[key] = value

    validate: ->
        if @strictMode is not true
            return true
        for key in Object.keys(@defined_properties)
            if this[key] is undefined
                throw Error 'Missing input'

    format_string: (value) ->
        if value.constructor isnt String
            throw Error 'Wrong type'
        return value

    format_boolean: (value) ->
        if value.constructor isnt Boolean
            throw Error 'Wrong type'
        return value

    format_integer: (value) ->
        if value.constructor isnt Number
            throw Error 'Wrong type'
        return value

    format_short: (value) ->
        if value.constructor isnt Number or value >= 32768 or value <= -32768
            throw Error 'Wrong type'
        return value

    format_long: (value) ->
        if value.constructor isnt Number
            throw Error 'Wrong type'
        return value

    format_date: (value) ->
        if value.constructor isnt Date
            throw Error 'Wrong type'
        return value

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



module.exports = GraphEntity