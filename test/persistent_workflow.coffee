chai = require('chai')
chaiAsPromised = require('chai-as-promised')
expect = chai.expect
winston = require('winston')
config = require('../config')
chai.use(chaiAsPromised)
chai.should()
Oriento = require 'oriento'
randomId = require '../lib/randomid'
server = Oriento()
GraphEntity = require '../lib/models/GraphEntity'
config = require '../config'
fs = require 'fs'
Promise = require 'bluebird'
libxmljs = require 'libxmljs'
_ = require 'lodash'

UserTask = require '../lib/models/vertexes/UserTask'
ScriptTask = require '../lib/models/vertexes/ScriptTask'

testXmlFilePath = __dirname + '/TestWorkflowSpec.bpmn'

namespace_prefixes =
    bpmn2: 'http://www.omg.org/spec/BPMN/20100524/MODEL'
    camunda: 'http://activiti.org/bpmn'

class TestGraphObject extends GraphEntity
    name: 'Workflow'
    superClass: 'V'
    builtin: false
    schema: true
    strictMode: true
    defined_properties: {
        name: 'string'
        id: 'string'
        fa: 'link'
    }



readXmlFromFile = (filepath) ->
    return new Promise (resolve, reject) ->
        filedata = fs.readFileSync(filepath, 'ascii')
        xmldoc = libxmljs.parseXmlString(filedata)
        resolve(xmldoc)

filterXmlToJustProcess = (xmldoc) ->
    return new Promise (resolve, reject) ->
        resolve xmldoc.get('//bpmn2:process', namespace_prefixes)


class WorflowDefinitionBuilder
    constructor: (database, xml) ->
        @db = database
        @xml = xml

    create_user_task: (xml_node) =>
        usertask = new UserTask
        usertask.set('name', xml_node.attr('name').value())
        usertask.set('id', xml_node.attr('id').value())
        return usertask.create(@db)

    create_script_task: (xml_node) =>
        scripttask = new ScriptTask
        scripttask.set('name', xml_node.attr('name').value())
        scripttask.set('id', xml_node.attr('id').value())
        return scripttask.create(@db)

    process_vertexes: ->
        vertexes = []

        user_tasks = @xml.find('//bpmn2:userTask', namespace_prefixes).map(@create_user_task)
        script_tasks = @xml.find('//bpmn2:scriptTask', namespace_prefixes).map(@create_script_task)
        vertexes = vertexes.concat(user_tasks, )
        return Promise.settle(vertexes)



describe 'Persistent Workflow usage principals', ->
    server_config = config.orient_db_config
    server = Oriento(server_config)

    before ->
        @xmlfile = readXmlFromFile(testXmlFilePath)

        @db_name = 'test_' + randomId()
        return server.create({
            name: @db_name,
            type: 'graph',
            storage: 'memory'})
        .then (database) =>
            @db = database
        .then =>
            usertask = new UserTask
            return usertask.updateSchema(@db)
        .then =>
            scripttask = new ScriptTask
            return scripttask.updateSchema(@db)
    after ->
        server.drop({
            name: @db_name
        })

    it 'should be able to get parse bpmn xml file with zero errors', ->
        expect(@xmlfile).eventually.to.have.deep.property('errors').length(0)

    it 'should be able to filter for just the process definition', ->
        xml = @xmlfile
            .then filterXmlToJustProcess
            .then (xmldoc) ->
                return xmldoc.attr('id').value()
        expect(xml).eventually.to.eql('workflow')

    it 'should be able to be able to build a workflow diagram', ->
        @xmlfile
            .then filterXmlToJustProcess
            .then (xml) =>
                return new WorflowDefinitionBuilder(@db, xml)
            .tap (builder) ->
                builder.process_vertexes()
