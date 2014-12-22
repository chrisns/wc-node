chai = require 'chai'
chaiAsPromised = require 'chai-as-promised'
expect = chai.expect
config = require '../config'
chai.use(chaiAsPromised)
chai.should()
Oriento = require 'oriento'
randomId = require '../lib/randomid'
config = require '../config'
Promise = require 'bluebird'
libxmljs = require 'libxmljs'
_ = require 'lodash'
WorflowDefinitionBuilder = require '../lib/WorkflowDefinitionBuilder'
fs = Promise.promisifyAll require 'fs'
namespace_prefixes = require '../lib/namespace_prefixes'

testXmlFilePath = __dirname + '/fixtures/TestWorkflowSpec.bpmn'


readXmlFromFile = (filepath) ->
    fs.readFileAsync(filepath)
        .then libxmljs.parseXmlString

filterXmlToJustProcess = (xmldoc) ->
    xmldoc.get('//bpmn2:process', namespace_prefixes)


createTestDatabase = (scope) ->
    scope.server = Oriento(config.orient_db_config)
    scope.db_name = 'test_' + randomId()
    scope.server.create
        name: scope.db_name
        type: 'graph'
        storage: 'memory'
    .tap (database) =>
#        scope.server.logger.debug = console.log.bind(console, '[orientdb]')
        scope.db = database

dropTestDatabase = (scope) ->
    scope.server.drop
        name: scope.db_name

describe 'Persistent Workflow DB Schema', ->
    beforeEach ->
        createTestDatabase(this)


    afterEach ->
        dropTestDatabase(this)

    it 'it should be able to write the schema', ->
        builder = new WorflowDefinitionBuilder(@db, null)
        class_list = builder.create_schema()
        .bind @db.class.list
        expect(class_list).eventually.to.have.length(11)

describe 'BPMN xml parser', ->
    beforeEach ->
        @xmlfile = readXmlFromFile(testXmlFilePath)

    it 'should be able to get parse bpmn xml file with zero errors', ->
        expect(@xmlfile).eventually.to.have.deep.property('errors').length(0)

    it 'should be able to filter for just the process definition', ->
        xml = @xmlfile
        .then filterXmlToJustProcess
        .then (xmldoc) ->
            return xmldoc.attr('id').value()
        expect(xml).eventually.to.eql('workflow')


describe 'Persistent Workflow builder principals', ->

    beforeEach ->
        xmlfile = readXmlFromFile(testXmlFilePath)
            .then filterXmlToJustProcess
            .then (xml) =>
                @xml = xml

        database = createTestDatabase(this)
        Promise.join(xmlfile, database)
            .then =>
                @builder = new WorflowDefinitionBuilder(@db, @xml)
                @builder.create_schema()

    afterEach ->
        dropTestDatabase(this)


    it 'should be able to be able to build a workflow diagram', ->
        entities = @builder.process_vertexes()
            .then =>
                @builder.process_edges()
            .then =>
                Promise.join(
                    @db.select('count(*)').from('V').scalar()
                    @db.select('count(*)').from('E').scalar()
                )
        expect(entities).eventually.to.eql([18, 12])


    xit 'it should be able to create a form field'

    xit 'it should be able to create a form field value'
    xit 'it should be ablt to create a user task'
    xit 'it should be able to create a script task'
    xit 'it should be able to create an exclusive gateway'
    xit 'it should be able to create a workflow start event'
    xit 'it should be able to create a workflow end event'
    xit 'it should be able to process all vertex creations'
    xit 'it should be able to process all edge creations'
    xit 'it should be able to an rid from an xml id'
    xit 'it should bee able to create a sequence flow'
    xit 'it should be able to find the next workflow step'
    xit 'it should be able to complete a workflow step'
    xit 'it should follow the right path from a conditional step'
