GraphEntity = GraphEntity('GraphEntity')

class Edge extends GraphEntity
    Name: 'E'
    builtin: true



module.exports = Edge
###

class Edge(GraphObject):
    def create(self):
        l.info('Creating class %s as an extension of %s' % (self.className, self.extendsClassName))
        self.commands.append("CREATE CLASS %s EXTENDS %s;" % (self.className, self.extendsClassName))

        for defined_property in self.defined_properties.items():
            l.info('Creating property %s.%s of type %s' % (self.className, defined_property[0], defined_property[1]))
            self.commands.append("CREATE PROPERTY %s.%s %s" %
                                 (self.className, defined_property[0], defined_property[1]))
        return self.commands

###