# =================================================================================================
# Script [master]:
#   /srv/salt/_grains/get_instance_ip_grains.py
# Usage:
#   > salt 'ops' saltutil.sync_grains
#     ops:
#       - grains.get_ops_env_grains
#   > salt 'ops' grains.items
#   . . .
#   ops_env:
#       ----------
#       auth_url:
#           http://10.9.60.88:5000/v2.0
#       pwd:
#           BlueC0at
#       region_name:
#           RegionOne
#       tenant_name:
#           admin
#       user:
#           admin
#   > salt 'ops' grains.get ops_env:region_name
#     ops:
#       RegionOne
# =================================================================================================

#!/usr/bin/env python
import subprocess
import logging

log = logging.getLogger(__name__)

def get_instance_ip_grains ():
  log.trace('Setting [ops_env] grains')

  int_ip = subprocess.Popen("nova show cloud_ns_main-185391-1 | grep network | cut -d\| -f3 | cut -d, -f1", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  ext_ip = subprocess.Popen("nova show cloud_ns_main-185391-1 | grep network | cut -d\| -f3 | cut -d, -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

  # Initialize an "grains" dictionary
  grains = {}

  # Append items to the "ops_env" grains
  grains['ops_env'] = {'int_ip': int_ip,\
                       'ext_ip': ext_ip}

  return grains