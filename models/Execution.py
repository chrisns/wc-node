#!/usr/bin/env python
# coding=utf-8
"""Execution model"""

from google.appengine.ext import ndb


class StoredValues(ndb.Model):
    """
    model for keeping an index of values we want to be able to index and search by
    """
    k = ndb.StringProperty(indexed=True)
    v = ndb.PickleProperty(indexed=True)


class Execution(ndb.Model):
    """Models an individual execution"""
    created = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty(compressed=True)
    values = ndb.StructuredProperty(StoredValues, repeated=True, indexed=True)

    @property
    def execution_id(self):
        """
        get the urlsafe execution id within the model
        @return:
        """
        return self._key.urlsafe() if hasattr(self._key, 'urlsafe') else None