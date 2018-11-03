# =========================================================
# Script:
#   check_cc_status.py
# Usage:
#   python check_cc_status.py -i dk-ccs-dk1-0 -n 7
#   python check_cc_status.py -i dk-ccs-dk1-0 -n 7 -o 0
#   python check_cc_status.py --instance dk-ccs-dk1-0 --nodes 7 --output 1
# Example:
#   python check_cc_status.py -i dk-ccs-dk1-0 -n 7 -o 1
#     Running the command... Please wait
#     ['UN', '192.168.99.57', '385.26', 'KB', '256', '27.9%', 'd30e0cc0-4b37-44d4-8590-16eb592536af', 'rack1']
#     ['UN', '192.168.99.235', '495.05', 'KB', '256', '29.2%', 'cfb58513-6954-48a2-8562-c035a962796f', 'rack1']
#     ['UN', '192.168.99.237', '467.15', 'KB', '256', '28.1%', 'fec3baa3-edeb-471f-b297-2a1249c1b090', 'rack1']
#     ['UN', '192.168.99.240', '516.16', 'KB', '256', '28.4%', '6de686f3-af07-4a30-af89-e6848c84ec88', 'rack1']
#     ['UN', '192.168.99.242', '493.62', 'KB', '256', '28.0%', 'f6277256-110e-42db-a069-4d03203372f3', 'rack1']
#     ['UN', '192.168.99.51', '374.81', 'KB', '256', '29.7%', 'cb14a659-b41a-462d-b7e2-f1e1357dbfb4', 'rack1']
#     ['UN', '192.168.99.55', '359.67', 'KB', '256', '28.8%', '2bb8955a-9536-4a65-9236-7f16dace869c', 'rack1']
#     Success
# =========================================================
#!/usr/bin/python

import sys, getopt
import subprocess


def main(argv):

  show_output = 0

  try:
    opts, args = getopt.getopt(argv,"hi:n:o:",["instance=","nodes=","output="])
  except getopt.GetoptError:
    print 'check_cc_state.py -h <host_name> -n <number_of_nodes> -o <show_output: [0|1]'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'check_cc_state.py -i <instance_name> -n <number_of_nodes> -o <show_output: [0|1]>'
      sys.exit()
    elif opt in ("-i", "--instance"):
      instance_name = arg
    elif opt in ("-n", "--nodes"):
      number_of_nodes = arg
    elif opt in ("-o", "--output"):
      show_output = arg

  if int(show_output) >= 1 or int(show_output) < 0:
    show_output = 1

  cmd = "salt '" + instance_name + "' cmd.run \"runuser -l -s /bin/bash cassandra -c 'nodetool status notifications'\""
  print "Running the command... Please wait"
  # cmd = "cat nodetool_output.log"
  try:
    output = subprocess.check_output(cmd, shell=True)
  except subprocess.CalledProcessError as e:
    print e.output
    sys.exit()

  num_un_nodes = 0
  result = "Success"

  for outStr in output.split('\n'):
    if '% ' in outStr:
      strTokens = outStr.split( )
      # Aggregate the number of nodes
      if strTokens[0] == "UN":
        num_un_nodes += 1
      if int(show_output) == 1:
        print strTokens
      prcTokens = strTokens[5].split('.')
      # Check data distribution
      if int(prcTokens[0]) < 10 or int(prcTokens[0]) > 50:
        result = "Falure: nodes was not balanced"
        print(result)
        sys.exit()

  # Check the number of nodes
  if num_un_nodes > 0:
    if num_un_nodes < int(number_of_nodes):
      result = "Falure: only %s nodes are up and running"%(num_un_nodes)
      print(result)
      sys.exit()
  else:
    result = "Falure: nodes was not founded"

  print(result)

if __name__ == "__main__":
  main(sys.argv[1:])
  