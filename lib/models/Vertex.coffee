GraphEntity = require('./GraphEntity')
_ = require 'lodash'

class Vertex extends GraphEntity
    Name: 'V'
    builtin: true

    create: (db) ->
        @inbuilt_properties =
            '@class': @Name
        merged_properties = _.extend(@inbuilt_properties, @properties)
        return db.vertex.create(merged_properties)


module.exports = Vertex
