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
Workflow = require '../lib/models/vertexes/Workflow'
WorkflowEndEvent = require '../lib/models/vertexes/WorkflowEndEvent'
NextStep = require '../lib/models/edges/NextStep'

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
        if xml_node.attr('label')?
            formfield.set('label', xml_node.attr('label').value())
        if xml_node.attr('type')?
            formfield.set('type', xml_node.attr('type').value())
        if xml_node.get('//camunda:property[@id="weight"]', namespace_prefixes)?
            formfield.set('weight', parseInt(xml_node.get('//camunda:property[@id="weight"]', namespace_prefixes).attr('value').value()))
        form_field_values = xml_node.find('//camunda:value', namespace_prefixes)
#        TODO: handle default value and edges
        formfield.create(@db)
            .return form_field_values
            .map @create_form_field_value

    create_form_field_value: (xml_node) =>
        formfieldvalue = new FormFieldValue
        formfieldvalue.set('name', xml_node.attr('name').value())
        formfieldvalue.set('id', xml_node.attr('id').value())
        return formfieldvalue.create(@db)

    create_user_task: (xml_node) =>
        usertask = new UserTask
        usertask.set('name', xml_node.attr('name').value())
        usertask.set('id', xml_node.attr('id').value())
        fields = xml_node.find('//camunda:formField', namespace_prefixes)
        usertask.create(@db)
            .return fields
            .map @create_form_field
            .then ->
                return true

    create_script_task: (xml_node) =>
        scripttask = new ScriptTask
        scripttask.set('name', xml_node.attr('name').value())
        scripttask.set('id', xml_node.attr('id').value())
        scripttask.set('script', xml_node.get('bpmn2:script', namespace_prefixes)?.text())
        return scripttask.create(@db)

    create_exclusive_gateway: (xml_node) =>
        exclusivegateway = new ExclusiveGateway
        exclusivegateway.set('name', xml_node.attr('name').value())
        exclusivegateway.set('id', xml_node.attr('id').value())
        #TODO: handle default flow
        return exclusivegateway.create(@db)

    create_workflow: (xml_node) =>
        workflow = new Workflow
        workflow.set('id', xml_node.attr('id').value())
        return workflow.create(@db)

    create_workflowend: (xml_node) =>
        workflowend = new WorkflowEndEvent
        workflowend.set('id', xml_node.attr('id').value())
        return workflowend.create(@db)

    process_vertexes: ->
        vertexes = [
            Promise.settle @xml.find('//bpmn2:startEvent', namespace_prefixes).map(@create_workflow)
            Promise.settle @xml.find('//bpmn2:endEvent', namespace_prefixes).map(@create_workflowend)
            Promise.settle @xml.find('//bpmn2:scriptTask', namespace_prefixes).map(@create_script_task)
            Promise.settle @xml.find('//bpmn2:exclusiveGateway', namespace_prefixes).map(@create_exclusive_gateway)
            Promise.settle @xml.find('//bpmn2:userTask', namespace_prefixes).map(@create_user_task)
        ]
        Promise.settle vertexes

    create_sequence_flow: (xml_node) =>
        from_id = xml_node.attr('sourceRef').value()
        to_id = xml_node.attr('targetRef').value()
        condition = xml_node.get('bpmn2:conditionExpression', namespace_prefixes)?.text()
        from = @db.select('@rid').from('V').where({id:from_id}).limit(1).one()
        to = @db.select('@rid').from('V').where({id:to_id}).limit(1).one()

        Promise.join from, to, (from, to) =>
            if not from?
                throw Error "#{from_id} does not exist"
            if not to?
                throw Error "#{to_id} does not exist"
            nextstep = new NextStep
            nextstep.from = from
            nextstep.to = to
            nextstep.set('id', xml_node.attr('id').value())
            if condition?
                nextstep.set('condition', condition)
            return nextstep.create(@db)

    process_edges: ->
        return Promise.settle @xml.find('//bpmn2:sequenceFlow', namespace_prefixes).map(@create_sequence_flow)


createSchema = (db) ->
    graph_classes = [
        UserTask
        ScriptTask
        FormField
        FormFieldValue
        ExclusiveGateway
        NextStep
        Workflow
        WorkflowEndEvent
    ]
    classCreationPromises = []
    for graph_class in graph_classes by 1
        graphClass = new graph_class
        classCreationPromises.push(graphClass.updateSchema(db))
    return Promise.settle classCreationPromises

describe 'Persistent Workflow usage principals', ->
    server_config = config.orient_db_config

    beforeEach ->
        @xmlfile = readXmlFromFile(testXmlFilePath)
        @graphObject = new TestGraphObject
        @server = Oriento(server_config)
        @db_name = 'test_' + randomId()
        return @server.create
            name: @db_name
            type: 'graph'
            storage: 'memory'
        .tap (database) =>
#            @server.logger.debug = console.log.bind(console, '[orientdb]')
            @db = database
        .tap createSchema

    afterEach ->
        @server.drop
            name: @db_name

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
#            .tap (builder) ->
#                builder.process_edges()

