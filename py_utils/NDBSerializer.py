# -*- coding: utf-8 -*-
from __future__ import division
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.storage.Serializer import Serializer
from SpiffWorkflow.operators import Attrib

_dictserializer = DictionarySerializer()



class NDBSerializer(Serializer):

    def serialize_workflow(self, workflow, **kwargs):
        thedict = _dictserializer.serialize_workflow(workflow, **kwargs)
        return thedict

    def deserialize_workflow(self, workflow, **kwargs):
        thedict = s_state
        return _dictserializer.deserialize_workflow(thedict, **kwargs)
