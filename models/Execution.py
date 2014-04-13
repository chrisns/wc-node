#!/usr/bin/env python
"""Execution model"""
import sys
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine")
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/lib/yaml/lib")
sys.path.append("remotes/endpoints-proto-datastore")
from google.appengine.ext import ndb

class Execution(ndb.Expando):
    """Models an individual execution"""
    owner = ndb.IntegerProperty(required=True)