# =================================================================================================
# Script [master]:
#   /srv/salt/_grains/get_ops_db_grains.py
# Usage:
#   > salt 'ops' saltutil.sync_grains
#     ops:
#       - grains.get_ops_db_grains
#   > salt 'ops' grains.items
#   . . .
#   ops_db:
#       ----------
#       host:
#           10.9.60.88
#       pwd:
#           7c592d3dc8514fa3
#       user:
#           root
#   > salt 'ops' grains.get ops_db:host
#     ops:
#       10.9.60.88
# =================================================================================================

#!/usr/bin/env python
import subprocess
import logging

log = logging.getLogger(__name__)

def gen_ops_db_grains ():
  log.trace('Setting [ops_db] grains')

  db_host = subprocess.Popen("cat /root/answer_file.txt | egrep ^CONFIG_MARIADB_HOST | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  db_user = subprocess.Popen("cat /root/answer_file.txt | egrep ^CONFIG_MARIADB_USER | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
  db_pwd  = subprocess.Popen("cat /root/answer_file.txt | egrep ^CONFIG_MARIADB_PW | cut -d= -f2", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

  # Initialize a "grains" dictionary
  grains = {}

  # Append items to the "ops_db" grains
  grains['ops_db'] = {'host': db_host, \
                      'user': db_user, \
                      'pwd': db_pwd}

  return grains
  