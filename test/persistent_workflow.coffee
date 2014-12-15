chai = require('chai')
chaiAsPromised = require('chai-as-promised')
expect = chai.expect
winston = require('winston')
config = require('../config')
chai.use(chaiAsPromised)
chai.should()
randomId = require('../lib/randomid')
Oriento = require('oriento')
randomId = require('../lib/randomid')
server = Oriento()
GraphEntity = require('../lib/models/GraphEntity')
config = require('../config')
fs = require 'fs'
#xml2js = require('xml2js').Parser()
Promise = require("bluebird")
libxmljs = require("libxmljs")
#xpath = require('xpath')
#DOMParser = require('xmldom').DOMParser
_ = require('lodash')

UserTask = require '../lib/models/vertexes/UserTask'

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
        xmldoc = libxmljs.parseXmlString(filedata);
        resolve(xmldoc)

filterXmlToJustProcess = (xmldoc) ->
    return new Promise (resolve, reject) ->
        # common practice appears to have the process first then the diagram, if we
        # found a time where this didn't happen we'd need to filter more inteligently
        # here, but for the sake of speed we make this assumption
        resolve xmldoc.get('//bpmn2:process', namespace_prefixes)


class WorflowDefinitionBuilder
    constructor: (database, xml) ->
        @db = database
        @xml = xml

#        @process_vertexes()
#        console.log(xml)
#        add_to_graph(name="StartEvent_1", obj=Workflow())
#        add_to_graph(name="EndEvent_1", obj=WorkflowEndEvent())

    create_user_task: (xml_node) =>
        usertask = new UserTask
        usertask.set('name', xml_node.attr('name').value())
        usertask.set('id', xml_node.attr('id').value())
        console.log(usertask.create(@db))
        return usertask.create(@db)


    process_vertexes: ->
#        new Promise (resolve, reject) =>
#            console.log(@xml)
#            console.log(@db)
#            user_tasks = _.map(@xml.find('//bpmn2:userTask', namespace_prefixes), @create_user_task)
        user_tasks = @xml.find('//bpmn2:userTask', namespace_prefixes).map(@create_user_task)
#            console.log(user_tasks)
        return Promise.settle(user_tasks)
#            resolve()

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

    xit 'should be able to be able to build a workflow diagram', ->
#        @timeout(10000)
        @xmlfile
            .then filterXmlToJustProcess
            .then (xml) =>
                return new WorflowDefinitionBuilder(@db, xml)
            .tap (builder) ->
                builder.process_vertexes()
#    it 'should provide a valid definition', ->
#        readXmlFromFile(__dirname + '/TestWorkflowSpec.bpmn')
#            .then filterXmlToJustProcess
#            .then make
#            .then (response) ->
#                console.dir(response)
#                console.dir result