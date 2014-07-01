#!/usr/bin/env python
# coding=utf-8
"""Execution model"""

from google.appengine.ext import ndb


class Execution(ndb.Expando):

    """Models an individual execution"""
    created = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty()

    @property
    def execution_id(self):
        return self._key.urlsafe() if hasattr(self._key, 'urlsafe') else None

    # @classmethod
    # def execution_id(self):
    #     print self._key
    #     self._key.urlsafe()
    @classmethod
    def listByOwner(cls, owner_id):
      return cls.query(owner = owner_id)