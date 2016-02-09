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

def peek_blacklist():
  try:
    blacklist = requests.head(url)

    if blacklist.status_code == 200:
      return blacklist.headers['Last-Modified']
    else:
      sys.exit(0)
  except:
    sys.exit(0)

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
    if re.match(r'^127.0.0.1', line):
      bad_hosts.append(line)

  if len(bad_hosts) == 0:
    sys.exit(0)
  else:
    return bad_hosts

def hosts_updated(last_modified):
  fh = open(system_hosts, 'r')
  data = fh.read()
  fh.close()
  hosts = data.split(lf)
  for line in hosts:
    if re.match(r'^# Last updated: .*$', line):
      this_version = re.sub(r'^# Last updated: (.*)$', '\\1', line)
      if this_version == last_modified:
        return False
      else:
        return True
    # return True if line not found
  return True

def write_to_etc_hosts(last_modified, bad_hosts):
  etc_hosts = open(system_hosts, 'a')
  etc_hosts.write('# adhostblocker' + lf)
  etc_hosts.write('# Last updated: ' + last_modified + lf)
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
  last_modified = peek_blacklist()
  if hosts_updated(last_modified):
    rawlist = get_blacklist()
    bad_hosts = parse_hosts(rawlist)
    reset_etc_hosts()
    write_to_etc_hosts(last_modified, bad_hosts)

if __name__ == '__main__':
  main()
