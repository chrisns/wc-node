chai = require("chai");
chaiAsPromised = require("chai-as-promised");
expect = chai.expect;
winston = require('winston');
config = require('../config');
chai.use(chaiAsPromised);
chai.should();

class GraphEntity
    builtin: true
    getDefinition: ->
        return @name


class Vertex extends GraphEntity
    name: 'V'
    builtin: true


class Workflow extends Vertex
    name: 'Workflow'
    builtin: false
    schema: true



describe 'Model usage principals', ->
    it 'Database should exist', ->
        workflow1 = new Workflow
        console.log(workflow1.getDefinition())
        return true
