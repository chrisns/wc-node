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
    inputs_required = messages.StringField(2, required=True)



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





class execution_resume_response(messages.Message):
    """ API Response data class """
    execution_id = messages.StringField(1, required=False)
    workflow_step = messages.StringField(2, repeated=True)
    user_message = messages.StringField(3, repeated=True)
    inputs_required = messages.StringField(4, required=True)




class service_status_response(messages.Message):
    ndb = messages.IntegerField(1, required=True)
    fb = messages.IntegerField(2, required=True)
