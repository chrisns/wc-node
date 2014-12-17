GraphEntity = require './GraphEntity'
_ = require 'lodash'

class Edge extends GraphEntity
    Name: 'E'
    builtin: true

    create: (db) ->
        @inbuilt_properties =
            '@class': @Name
        merged_properties = _.extend(@inbuilt_properties, @properties)
        db.edge.from(@from).to(@to).create(merged_properties)

module.exports = Edge
