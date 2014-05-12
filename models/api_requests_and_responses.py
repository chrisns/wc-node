#!/usr/bin/env python
"""Request and response models for the API"""

from protorpc import messages

class execution_list_request(messages.Message):
    """ for execution_list() """
    user_id = messages.IntegerField(1, required=True)
    token = messages.StringField(2, required=True)

class execution_list_summary_response(messages.Message):
    """ for execution_list() """
    execution_id = messages.StringField(1, required=True)

class execution_list_response(messages.Message):
    """ for execution_list() """
    executions = messages.MessageField(execution_list_summary_response, 1, repeated=True)



class execution_new_request(messages.Message):
    """ for execution_new() """
    user_id = messages.IntegerField(1, required=True)
    token = messages.StringField(2, required=True)


class execution_new_response(messages.Message):
    """ for execution_new() """
    inputs_required = messages.StringField(1, repeated=True)



class execution_delete_request(messages.Message):
    """ for execution_delete() """
    user_id = messages.IntegerField(1, required=True)
    token = messages.StringField(2, required=True)
    execution_id = messages.StringField(3, required=True)

class execution_list_data_request(messages.Message):
    """ for execution_resume() """
    key = messages.StringField(1, required=True)
    value = messages.StringField(2, repeated=True)

class execution_resume_request(messages.Message):
    """ for execution_resume() """
    user_id = messages.IntegerField(1, required=True)
    token = messages.StringField(2, required=True)
    execution_id = messages.StringField(3, required=False)
    data = messages.MessageField(execution_list_data_request, 4, repeated=True)

class input_option(messages.Message):
    name = messages.StringField(1, required=True)
    value = messages.StringField(2, required=True)

class input(messages.Message):
    name = messages.StringField(1, required=True)
    label = messages.StringField(2)
    input_type = messages.StringField(3, required=True)
    placeholder = messages.StringField(4)
    description = messages.StringField(5)
    options = messages.MessageField(input_option, 6, repeated=True)
    validator = messages.StringField(7)
    autocomplete_path = messages.StringField(8)
    default_value = messages.StringField(8)



class execution_resume_response(messages.Message):
    """ API Response data class """
    execution_id = messages.StringField(1, required=False)
    workflow_step = messages.StringField(2, repeated=True)
    user_message = messages.StringField(3, repeated=True)
    inputs_required = messages.StringField(4, repeated=True)