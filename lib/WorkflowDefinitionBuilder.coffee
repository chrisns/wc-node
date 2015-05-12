Promise = require 'bluebird'

namespace_prefixes = require './namespace_prefixes'
UserTask = require '../lib/models/vertexes/UserTask'
ScriptTask = require '../lib/models/vertexes/ScriptTask'
FormField = require '../lib/models/vertexes/FormField'
FormFieldValue = require '../lib/models/vertexes/FormFieldValue'
ExclusiveGateway = require '../lib/models/vertexes/ExclusiveGateway'
Workflow = require '../lib/models/vertexes/Workflow'
WorkflowEndEvent = require '../lib/models/vertexes/WorkflowEndEvent'
NextStep = require '../lib/models/edges/NextStep'
Includes = require '../lib/models/edges/Includes'
HasPredefinedAnswerOf = require '../lib/models/edges/HasPredefinedAnswerOf'
HasDefaultAnswerOf = require '../lib/models/edges/HasDefaultAnswerOf'

class WorflowDefinitionBuilder
    constructor: (database, xml) ->
        @db = database

        if xml?
            @xml = xml
            @xml._find = xml.find
            @xml.find = (lookup) =>
                return @xml._find(lookup, namespace_prefixes)

    create_schema: =>
        graph_classes = [
            UserTask
            ScriptTask
            FormField
            FormFieldValue
            ExclusiveGateway
            NextStep
            Workflow
            WorkflowEndEvent
            Includes
            HasPredefinedAnswerOf
            HasDefaultAnswerOf
        ]
        classCreationPromises = []
        for graph_class in graph_classes by 1
            graphClass = new graph_class
            classCreationPromises.push(graphClass.updateSchema(@db))
        return Promise.settle classCreationPromises

    create_form_field: (xml_node) =>
        formfield = new FormField
        formfield.set('id', xml_node.attr('id').value())
        if xml_node.attr('label')?
            formfield.set('label', xml_node.attr('label').value())
        if xml_node.attr('type')?
            formfield.set('type', xml_node.attr('type').value())
        if xml_node.get('//camunda:property[@id="weight"]', namespace_prefixes)?
            formfield.set('weight',
                parseInt(xml_node.get('//camunda:property[@id="weight"]', namespace_prefixes).attr('value').value())
            )
        formfield.create(@db)

    create_form_field_in_edge: (xml_node) =>
        from_id = xml_node.get('ancestor::bpmn2:userTask', namespace_prefixes).attr('id').value()
        to_id = xml_node.attr('id').value()
        from = @_get_rid_from_id(from_id)
        to = @_get_rid_from_id(to_id)
        includes = new Includes
        @_create_edge(from, to, includes)

    create_form_field_value_in_edge: (xml_node) =>
        from_id = xml_node.get('ancestor::camunda:formField', namespace_prefixes).attr('id').value()
        to_id = xml_node.attr('id').value()
        from = @_get_rid_from_id(from_id)
        to = @_get_rid_from_id(to_id)
        answer_of = new HasPredefinedAnswerOf
        @_create_edge(from, to, answer_of)

    create_form_field_default_value_in_edge: (xml_node) =>
        from_id = xml_node.attr('id').value()
        to_id = xml_node.attr('defaultValue').value()
        from = @_get_rid_from_id(from_id)
        to = @_get_rid_from_id(to_id)
        answer_of = new HasDefaultAnswerOf
        @_create_edge(from, to, answer_of)

    _create_edge: (from, to, edge) ->
        Promise.join from, to, (from, to) =>
            if not from?
                throw Error "#{from_id} does not exist"
            if not to?
                throw Error "#{to_id} does not exist"
            edge.from = from.rid
            edge.to = to.rid
            return edge.create(@db)

    create_form_field_value: (xml_node) =>
        formfieldvalue = new FormFieldValue
        formfieldvalue.set('name', xml_node.attr('name').value())
        formfieldvalue.set('id', xml_node.attr('id').value())
        return formfieldvalue.create(@db)

    create_user_task: (xml_node) =>
        usertask = new UserTask
        usertask.set('name', xml_node.attr('name').value())
        usertask.set('id', xml_node.attr('id').value())
        usertask.create(@db)

    create_script_task: (xml_node) =>
        scripttask = new ScriptTask
        scripttask.set('name', xml_node.attr('name').value())
        scripttask.set('id', xml_node.attr('id').value())
        scripttask.set('script', xml_node.get('bpmn2:script', namespace_prefixes).text())
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
            Promise.settle @xml.find('//bpmn2:startEvent').map(@create_workflow)
            Promise.settle @xml.find('//bpmn2:endEvent').map(@create_workflowend)
            Promise.settle @xml.find('//bpmn2:scriptTask').map(@create_script_task)
            Promise.settle @xml.find('//bpmn2:exclusiveGateway').map(@create_exclusive_gateway)
            Promise.settle @xml.find('//bpmn2:userTask').map(@create_user_task)
            Promise.settle @xml.find('//camunda:formField').map(@create_form_field)
            Promise.settle @xml.find('//camunda:value').map(@create_form_field_value)
        ]
        Promise.settle vertexes

    _get_rid_from_id: (id) =>
        @db.select('@rid').from('V').where({id: id}).limit(1).one()

    create_sequence_flow: (xml_node) =>
        from_id = xml_node.attr('sourceRef').value()
        to_id = xml_node.attr('targetRef').value()
        condition = xml_node.get('bpmn2:conditionExpression', namespace_prefixes)?.text()
        from = @_get_rid_from_id(from_id)
        to = @_get_rid_from_id(to_id)

        nextstep = new NextStep
        if condition?
            nextstep.set('condition', condition)
        nextstep.set('id', xml_node.attr('id').value())

        @_create_edge(from, to, nextstep)

    process_edges: ->
        edges = [
            Promise.settle @xml.find('//bpmn2:sequenceFlow').map(@create_sequence_flow)
            Promise.settle @xml.find('//camunda:formField').map(@create_form_field_in_edge)
            Promise.settle @xml.find('//camunda:value').map(@create_form_field_value_in_edge)
            Promise.settle @xml.find('//camunda:formField[@defaultValue]').map(@create_form_field_default_value_in_edge)
        ]
        return Promise.settle edges

module.exports = WorflowDefinitionBuilder