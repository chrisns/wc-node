GraphEntity = require('./GraphEntity')
_ = require 'lodash'

class Vertex extends GraphEntity
    Name: 'V'
    builtin: true

    create: (db) ->
        @inbuilt_properties =
            '@class': @Name
        return db.vertex.create(_.extend(@inbuilt_properties, @properties ))


module.exports = Vertex
###
class Vertex(GraphObject):
def create(self):
l.info('Creating class %s as an extension of %s' % (self.className, self.extendsClassName))
self.commands.append("CREATE CLASS %s EXTENDS %s;" % (self.className, self.extendsClassName))

if self.strictMode is True:
self.commands.append("ALTER CLASS %s STRICTMODE TRUE;" % self.className)

for defined_property in self.defined_properties.items():
l.info('Creating property %s.%s of type %s' % (self.className, defined_property[0], defined_property[1]))
self.commands.append("CREATE PROPERTY %s.%s %s" %
  (self.className, defined_property[0], defined_property[1]))
return self.commands
###