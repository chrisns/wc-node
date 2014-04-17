#!/usr/bin/env python
"""Execution model"""
import sys
sys.path.append("remotes/googleappeingine/python/lib/yaml/lib")
sys.path.append("remotes/googleappeingine/python")
from google.appengine.ext import ndb

class Execution(ndb.Expando):
    """Models an individual execution"""
    owner = ndb.IntegerProperty(required=True)
    data = ndb.PickleProperty()