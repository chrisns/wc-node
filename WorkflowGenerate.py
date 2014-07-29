#!/usr/bin/env python
# coding=utf-8
"""Workflow definition, not executed at runtime so needs to be done at build to generate json spec file"""

import os
import fnmatch
from io import BytesIO
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
        """
        Handles packaging a workflow in memory, bpmn normally likes to deserialize a zip
        @param workflow_name: the workflow process to use
        @param workflow_files: file name(s)
        @param editor: the editor that was used
        @return:
        """
        s = BytesIO()
        p = cls(s, workflow_name, meta_data=[], editor=editor)
        p.add_bpmn_files_by_glob(workflow_files)
        p.create_package()
        return s.getvalue()


class BpmnHelper(object):
    """
    provides various things to help with bpmn activities
    """
    @staticmethod
    def load_workflow_spec(found_file, process_name):
        """
        Override to deserialize in memory the workflow spec in memory
        @param found_file:
        @param process_name:
        @return:
        """
        f = os.path.join(os.path.dirname(__file__), found_file)

        return BpmnSerializer().deserialize_workflow_spec(
            MemoryPackager.package_in_memory(process_name, f))


if __name__ == '__main__':

    for file_name in os.listdir('WorkflowSpecs'):  # pragma: no cover
        if fnmatch.fnmatch(file_name, '*.bpmn'):  # pragma: no cover
            spec = BpmnHelper().load_workflow_spec('WorkflowSpecs/' + file_name, 'workflow')  # pragma: no cover
            print("outputting workflow to " + file_name[:-5] + ".JSON")  # pragma: no cover
            # noinspection Restricted_Python_calls,PyTypeChecker
            open("WorkflowSpecs/" + file_name[:-5] + ".json", "w").write(
                spec.serialize(JSONSerializer()))  # pragma: no cover
            # noinspection Restricted_Python_calls
            open("WorkflowSpecs/" + file_name[:-5] + ".dot", "w").write(
                spec.serialize(dotVisualizer()))  # pragma: no cover