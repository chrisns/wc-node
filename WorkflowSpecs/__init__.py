# -*- coding: utf-8 -*-
from __future__ import division
import sys

sys.path.append("./remotes/SpiffWorkflow")
sys.path.append("./remotes/gvgen")

from .Evaluate import Evaluate
from .UserInput import UserInput

import inspect
__all__ = [name for name, obj in list(locals().items())
           if not (name.startswith('_') or inspect.ismodule(obj))]
