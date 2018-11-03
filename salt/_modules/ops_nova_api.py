#!/usr/bin/env python
# =============================================================================
# Script [master]:
#   /srv/salt/ns/_modules/ops_nova_api.py
# Usage:
#   salt 'ops' saltutil.sync_modules
#   salt 'ops' -l debug ops_nova_api.get_next_floating_ip 'public'
#
# =============================================================================

from jinja2 import Environment, FileSystemLoader
from novaclient import client

import logging
log = logging.getLogger(__file__)

def get_next_floating_ip(pools):

  lib_version = 2
  os-username = str(__grains__['ops_env']['user']).strip('[]')
  os-password = str(__grains__['ops_env']['pwd']).strip('[]')
  os-tenant-name = str(__grains__['ops_env']['tenant_name']).strip('[]')
  os-auth-url = str(__grains__['ops_env']['auth_url']).strip('[]')

  nova = client.Client(lib_version, os-username, os-password, os-tenant-name, os-auth-url, service_type="compute")

  all_floating_ips = nova.floating_ips.list()

  for pool in pools:
    # temporary list per pool
    pool_ips = []
    # loop through all floating IPs
    for f_ip in all_floating_ips:
      # if not reserved and the correct pool, add
      if f_ip.instance_id is None and (f_ip.pool == pool):
        log.info ("Available Floating IP: %s" % (f_ip.ip))
        pool_ips.append(f_ip.ip)
        # only need one
        break

  # if the list is empty, add for this pool
  if not pool_ips:
    try:
      new_ip = nova.floating_ips.create(pool)
    except Exception, e:
      log.error ("Error: %s - %s." % (e.filename,e.strerror))
      log.info ("Unable to create floating ip")
    pool_ips.append(new_ip.ip)

  return pool_ips[0]

def test():
  '''Just a test function'''
  return True

env = Environment(loader=FileSystemLoader('/usr/lib/python2.7/site-packages/salt'))
env.globals['get_next_floating_ip'] = get_next_floating_ip

if __name__ == "__main__":
#   flip = get_next_floating_ip(['public'])
#   print flip
  test()
  