#!/usr/bin/env python
# coding=utf-8
"""Workflow definition, not executed at runtime so needs to be done at build to generate json spec file"""
from __future__ import division

import os
from io import BytesIO
import fnmatch

from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import dotVisualizer
from SpiffWorkflow.bpmn.storage.BpmnSerializer import BpmnSerializer
from SpiffWorkflow.bpmn.storage.Packager import Packager

from py_utils.bpmn_helpers import CustomBpmnParser


class MemoryPackager(Packager):
    """ packages bpmn in stream to a zip so that the bpmn parser takes it in
    """
    PARSER_CLASS = CustomBpmnParser

    @classmethod
    def package_in_memory(cls, workflow_name, workflow_files, editor='camunda'):
        s = BytesIO()
        p = cls(s, workflow_name, meta_data=[], editor=editor)
        p.add_bpmn_files_by_glob(workflow_files)
        p.create_package()
        return s.getvalue()


class BpmnHelper(object):
    @staticmethod
    def load_workflow_spec(filename, process_name):
        f = os.path.join(os.path.dirname(__file__), filename)

        return BpmnSerializer().deserialize_workflow_spec(
            MemoryPackager.package_in_memory(process_name, f))


if __name__ == '__main__':

    for file in os.listdir('WorkflowSpecs'):  # pragma: no cover
        if fnmatch.fnmatch(file, '*.bpmn'):  # pragma: no cover
            spec = BpmnHelper().load_workflow_spec('WorkflowSpecs/' + file, 'workflow')  # pragma: no cover
            print("outputting workflow to " + file[:-5] + ".JSON")  # pragma: no cover
            # noinspection Restricted_Python_calls,PyTypeChecker
            open("WorkflowSpecs/" + file[:-5] + ".json", "w").write(
                spec.serialize(JSONSerializer()))  # pragma: no cover
            open("WorkflowSpecs/" + file[:-5] + ".dot", "w").write(
                spec.serialize(dotVisualizer()))  # pragma: no cover