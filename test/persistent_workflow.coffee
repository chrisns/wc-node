chai = require 'chai'
chaiAsPromised = require 'chai-as-promised'
expect = chai.expect
winston = require 'winston'
config = require '../config'
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
FormField = require '../lib/models/vertexes/FormField'
FormFieldValue = require '../lib/models/vertexes/FormFieldValue'
ExclusiveGateway = require '../lib/models/vertexes/ExclusiveGateway'

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
    defined_properties:
        name: 'string'
        id: 'string'
        fa: 'link'



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

    create_form_field: (xml_node) =>
        formfield = new FormField
        formfield.set('id', xml_node.attr('id').value())
        formfield.set('label', xml_node.attr('label').value())
        formfield.set('type', xml_node.attr('type').value())
        formfield.set('weight', xml_node.get('//camunda:property[@id="weight"]', namespace_prefixes).attr('value').value())
#        TODO: handle default value
        return formfield.create(@db)
            .tap (formfield) =>
                xml_node.find('//camunda:value', namespace_prefixes).map(@create_form_field_value)

    create_form_field_value: (xml_node) =>
        formfieldvalue = new FormFieldValue
        formfieldvalue.set('name', xml_node.attr('name').value())
        formfieldvalue.set('id', xml_node.attr('id').value())
        return formfieldvalue.create(@db)

    create_user_task: (xml_node) =>
        usertask = new UserTask
        usertask.set('name', xml_node.attr('name').value())
        usertask.set('id', xml_node.attr('id').value())
        return usertask.create(@db)
            .tap (usertask) =>
                xml_node.find('//camunda:formField', namespace_prefixes).map(@create_form_field)

    create_script_task: (xml_node) =>
        scripttask = new ScriptTask
        scripttask.set('name', xml_node.attr('name').value())
        scripttask.set('script', xml_node.get('bpmn2:script', namespace_prefixes).text())
        return scripttask.create(@db)

    create_exclusive_gateway: (xml_node) =>
        exclusivegateway = new ExclusiveGateway
        exclusivegateway.set('name', xml_node.attr('name').value())
        exclusivegateway.set('id', xml_node.attr('id').value())
        #TODO: handle default flow
        return exclusivegateway.create(@db)

    process_vertexes: ->
        vertexes = []
        user_tasks = @xml.find('//bpmn2:userTask', namespace_prefixes).map(@create_user_task)
        script_tasks = @xml.find('//bpmn2:scriptTask', namespace_prefixes).map(@create_script_task)
        exclusive_gateways = @xml.find('//bpmn2:exclusiveGateway', namespace_prefixes).map(@create_exclusive_gateway)
        vertexes = vertexes.concat(user_tasks, script_tasks, exclusive_gateways)
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
        .tap (database) =>
            @db = database
        .tap =>
            graph_classes = [
                UserTask
                ScriptTask
                FormField
                FormFieldValue
                ExclusiveGateway
            ]
            classCreationPromises = []
            for graph_class in graph_classes
                classCreationPromises.push(new graph_class().updateSchema(@db))
            return Promise.settle(classCreationPromises)

    after ->
        server.drop({name: @db_name })

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


###

def process_sequence_flow(self, sequence_flow):

###