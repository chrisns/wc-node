# -*- coding: utf-8 -*-
from __future__ import division

# requires: https://github.com/stricaud/gvgen
import gvgen

from SpiffWorkflow.storage.Serializer import Serializer

class dotVisualizer(Serializer):
    def serialize_workflow_spec(self, wf_spec):
        nodes = set()
        linked = set()
        graph = gvgen.GvGen()
        parent = graph.newItem("Workflow")
        
        # these built in shapes are available: http://www.graphviz.org/doc/info/shapes.html
        graph.styleAppend("Cancel",          "shape", "oval")
        graph.styleAppend("CancelTask",      "shape", "oval")
        graph.styleAppend("Choose",          "shape", "diamond")
        graph.styleAppend("ExclusiveChoice", "shape", "diamond")
        graph.styleAppend("Execute",         "shape", "rect")
        graph.styleAppend("Gate",            "shape", "trapezium")
        graph.styleAppend("Join",            "shape", "invtriangle")
        graph.styleAppend("Merge",           "shape", "invtriangle")
        graph.styleAppend("MultiChoice",     "shape", "diamond")
        graph.styleAppend("MultiInstance",   "shape", "box")
        graph.styleAppend("ReleaseMutex",    "shape", "diamond")
        graph.styleAppend("Simple",          "shape", "rect")
        graph.styleAppend("StartTask",       "shape", "oval")
        graph.styleAppend("SubWorkflow",     "shape", "invhouse")
        graph.styleAppend("ThreadMerge",     "shape", "invtriangle")
        graph.styleAppend("ThreadSplit",     "shape", "triangle")
        graph.styleAppend("ThreadStart",     "shape", "oval")
        graph.styleAppend("Transform",       "shape", "rect")
        graph.styleAppend("Trigger",         "shape", "oval")

        # build graph with all the nodes first
        def recurisvelyAddNodes(task_spec):
            if task_spec in nodes:
                return
            task_spec.gv = graph.newItem(task_spec.name, parent)
            # add a default style for this class so that if we don't have one when we apply it doesn't break the GvGen library
            graph.styleAppend(task_spec.__class__.__name__, "ignore", "this")
            graph.styleApply(task_spec.__class__.__name__, task_spec.gv)
            nodes.add(task_spec)
            sub_specs = ([task_spec.spec.start] if hasattr(task_spec, 'spec') else []) + task_spec.outputs
            for t in sub_specs:
                recurisvelyAddNodes(t)

        # then link all the nodes together
        def recursive_linking(task_spec):
            if task_spec in linked:
                return
            linked.add(task_spec)
            sub_specs = ([task_spec.spec.start] if hasattr(task_spec, 'spec') else []) + task_spec.outputs
            for i, t in enumerate(sub_specs):
                graph.newLink(task_spec.gv, t.gv)
                recursive_linking(t)

        recurisvelyAddNodes(wf_spec.start)
        recursive_linking(wf_spec.start)
        return (graph.dot() if graph.dot() else '')