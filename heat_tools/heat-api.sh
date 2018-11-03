#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Heat API Server.

An OpenStack REST API to Heat.
"""

from oslo_log import log as logging

from heat.common.i18n import _LW

LOG = logging.getLogger(__name__)

LOG.warning(_LW('DEPRECATED: `heat-api` script is deprecated. Please use the '
                'system level heat binaries installed to start '
                'any of the heat services.'))

import os
import sys

# If ../heat/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
POSSIBLE_TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))

if os.path.exists(os.path.join(POSSIBLE_TOPDIR, 'heat', '__init__.py')):
    sys.path.insert(0, POSSIBLE_TOPDIR)

from heat.cmd import api

api.main()