#!/usr/bin/env python
# coding=utf-8
"""Execution model"""

from google.appengine.ext import ndb


class Execution(ndb.Expando):

    """Models an individual execution"""
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty()
