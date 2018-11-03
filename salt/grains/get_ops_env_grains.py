# =================================================================================================
# Script [master]:
#   /srv/salt/_grains/get_ops_env_grains.py
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

def gen_ops_env_grains ():
  log.trace('Setting [ops_env] grains')

  ops_user = subprocess.Popen("cat /root/keystonerc_admin | egrep OS_USERNAME | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  ops_pwd = subprocess.Popen("cat /root/keystonerc_admin | egrep OS_PASSWORD | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  ops_auth_url = subprocess.Popen("cat /root/keystonerc_admin | egrep OS_AUTH_URL | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  ops_tenant_name = subprocess.Popen("cat /root/keystonerc_admin | egrep OS_TENANT_NAME | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  ops_region_name = subprocess.Popen("cat /root/keystonerc_admin | egrep OS_REGION_NAME | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

  # Initialize an "grains" dictionary
  grains = {}

  # Append items to the "ops_env" grains
  grains['ops_env'] = {'user': ops_user,\
                       'pwd': ops_pwd, \
                       'auth_url': ops_auth_url, \
                       'tenant_name': ops_tenant_name, \
                       'region_name': ops_region_name}

  return grains
  