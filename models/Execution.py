#!/usr/bin/env python
# coding=utf-8
"""Execution model"""

from google.appengine.ext import ndb


class Execution(ndb.Expando):
    """Models an individual execution"""
    created = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty(compressed=True)
    # values = ndb.StructuredProperty(StoredValues, repeated=True, indexed=True)

    @property
    def execution_id(self):
        """
        get the urlsafe execution id within the model
        @return:
        """
        return self._key.urlsafe() if hasattr(self._key, 'urlsafe') else None

    def __setattr__(self, name, value):
        if (name.startswith('_') or
                isinstance(getattr(self.__class__, name, None), (ndb.Property, property)) or
                isinstance(value, ndb.Model) or isinstance(value, dict)):
            return super(Execution, self).__setattr__(name, value)
        elif isinstance(value, list) and isinstance(value[0], dict):
            prop = ndb.StructuredProperty(ndb.Expando, name, repeated=True, indexed=self._default_indexed)
        else:
            return super(Execution, self).__setattr__(name, value)
        prop._code_name = name
        self._properties[name] = prop
        prop._set_value(self, value)