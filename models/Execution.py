#!/usr/bin/env python
# coding=utf-8
"""Execution model"""

from google.appengine.ext import ndb


class Execution(ndb.Expando):

    """Models an individual execution"""
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty()
    @classmethod
    def listByOwner(cls, owner_id):
      return cls.query(owner = owner_id)