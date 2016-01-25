#!/usr/bin/env python2.7
import re, requests, sys, os, tempfile

'''
bad hosts taken from someonewhocares.org
maintained by Dan Pollock
hosts@someonewhocares.org
'''

url = 'http://someonewhocares.org/hosts/hosts'
system_hosts = '/etc/hosts'
lf = os.linesep

def get_blacklist():
  # quietly die if request cannot be made
  try:
    blacklist = requests.get(url)

    if blacklist.status_code != 200:
      sys.exit(0)
  except:
    sys.exit(0)

  return blacklist.text

def parse_hosts(blacklist):
  bad_hosts = []
  for line in blacklist.split(lf):
    if re.match(r'^# Last updated', line):
      # check if this is the same version we have
      if hosts_updated(line) is True:
        bad_hosts.insert(0, line)
        continue
      else:
        sys.exit(0)
    if re.match(r'^127.0.0.1', line):
      bad_hosts.append(line)

  if len(bad_hosts) == 0:
    sys.exit(0)
  else:
    return bad_hosts

def hosts_updated(new_date):
  fh = open(system_hosts, 'r')
  for line in fh.read().split(lf):
    if re.match(r'^# Last updated', line):
      if line == new_date:
        fh.close()
        return False
      else:
        fh.close()
        return True
    # return True if line not found
    return True

def write_to_etc_hosts(bad_hosts):
  etc_hosts = open(system_hosts, 'a')
  etc_hosts.write('# adhostblocker' + lf)
  for line in bad_hosts:
    etc_hosts.write(line + lf)
  etc_hosts.close()

def reset_etc_hosts():
  etc_hosts = open(system_hosts, 'r')
  data = etc_hosts.read().split(lf)
  etc_hosts.close()
  modified = 0
  for line in data:
    if re.match('^# adhostblocker$', line):
      modified = 1
      break
  if modified:
    keep = data[:data.index('# adhostblocker')]
    # we want to overwrite the file
    etc_hosts = open(system_hosts, 'w')
    for line in keep:
      etc_hosts.write(line + lf)
    etc_hosts.close()

def main():
  rawlist = get_blacklist()
  bad_hosts = parse_hosts(rawlist)
  reset_etc_hosts()
  write_to_etc_hosts(bad_hosts)

if __name__ == '__main__':
  main()
