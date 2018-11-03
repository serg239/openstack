[root@salt-master _modules]# cat cluster.py
#!/usr/bin/env python

# =============================================================================
# Script [master]:
#   /srv/salt/ns/_modules/cluster.py
# Usage:
#   salt 'ops' saltutil.sync_modules
#   salt 'ops' cluster.get_cassandra_cluster_ips
#   salt 'ops' cluster.set_cassandra_grains
# Salt state:
#   get-node-grains:
#     module.run:
#       - name: cluster.set_cassandra_grains
#       - require:
#         - cmd: create-stack
# =============================================================================
# [openstack-controller ~]# cat /etc/salt/grains
# nsccdc1-01:
#   public_ip: 10.9.60.189
#   deployment: dc1
#   private_ip: 192.168.99.249
#   deployment: dc1
#   node_type: seed
#   roles:
#     - database
#     - cassandra
#     - opscenter
#    . . .
# =============================================================================
# salt 'ops' saltutil.grains_refresh
#
# salt 'ops' grains.items
#   nsccdc1-01:
#       ----------
#       deployment:
#           dc1
#       node_type:
#           seed
#       private_ip:
#           192.168.99.249
#       public_ip:
#           10.9.60.189
#       roles:
#           - database
#           - cassandra
#           - opscenter
#   . . .
# =============================================================================

import subprocess
import logging

log = logging.getLogger(__name__)

def get_cassandra_cluster_ips():

  # conn_grains = {}
  ip_grains = {}

  cluster_name = __pillar__['cluster']['cluster_name']
  datacenter_name = __pillar__['cluster']['datacenter_name']
  cluster_name += datacenter_name

  ops_user = __grains__['ops_env']['user']
  ops_pwd = __grains__['ops_env']['pwd']
  ops_auth_url = __grains__['ops_env']['auth_url']
  ops_tenant_name = __grains__['ops_env']['tenant_name']

  # conn_grains[cluster_name] = {'user': ops_user, 'pwd': ops_pwd, 'auth_url': ops_auth_url, 'tenant': ops_tenant_name}
  # return conn_grains

  conn_str = 'heat --os-username ' + ops_user
  conn_str += ' --os-password ' + ops_pwd
  conn_str += ' --os-tenant-name ' + ops_tenant_name
  conn_str += ' --os-auth-url ' + ops_auth_url

  for instance_name in __pillar__['cluster']['ops_cassandra_instances']:

    # Floating IP
    cmd_str = ' output-show ' + cluster_name + ' ' + instance_name + '_public_ip'
    pub_exec_str = conn_str + cmd_str
    public_ip = subprocess.Popen(pub_exec_str, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

    # Private IP
    cmd_str = ' output-show ' + cluster_name + ' ' + instance_name + '_private_ip'
    pri_exec_str = conn_str + cmd_str
    private_ip = subprocess.Popen(pri_exec_str, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

    ip_grains[instance_name] = {'public_ip': public_ip, 'private_ip': private_ip}
    # str_dict[instance_name] = {'public_ip': pub_exec_str, 'private_ip': pri_exec_str}

  # return str_dict
  return ip_grains

def set_cassandra_custom_grains(dict):
  ret_code = False

  datacenter_name = __pillar__['cluster']['datacenter_name']

  res = ""
  for index, instance_name in enumerate(dict):
    res = res + instance_name + ":\n"
    ips = dict[instance_name]
    for ip in ips:
      ip_name = ips[ip]
      ip_str = ip + ": " + ip_name.replace('\"','')
      res = res + "  " + ip_str + '\n'
    res = res + "  deployment: " + datacenter_name + "\n"
    if 0 <= index < 2:
      res = res + "  node_type: seed\n"
    else:
      res = res + "  node_type: regular\n"
    res = res + "  roles:\n"
    res = res + "    - database\n"
    res = res + "    - cassandra\n"
    if index == 0:
      res = res + "    - opscenter\n"

  try:
    grains_file = open("/etc/salt/grains", "w")
    grains_file.write(res)
    grains_file.close()
    ret_code = True
  except IOError as e:
    log.error("I/O error({0}): {1}".format(e.errno, e.strerror))

  return ret_code

def set_cassandra_grains():
  ret_code = False
  instance_ips_dict = get_cassandra_cluster_ips()
  if instance_ips_dict:
    if set_cassandra_custom_grains(instance_ips_dict):
      ret_code = True
  return ret_code

def test():
  '''Just a test function'''
  return True