#!/usr/bin/env python2.7
import re, requests, sys, os, tempfile

# bad hosts taken from someonewhocares.org
url = 'http://someonewhocares.org/hosts/hosts'
lf = os.linesep

def get_blacklist():
  # quietly die if request cannot be made
  try:
    blacklist = requests.get(url)

    if blacklist.status_code != 200:
      sys.exit(0)
  except:
    sys.exit(0)

  bad_hosts = []
  for line in blacklist.text.split(lf):
    if re.match(r'^127.0.0.1', line):
      bad_hosts.append(line)
  if len(bad_hosts) == 0:
    sys.exit(0)
  return bad_hosts

def save_hosts(bad_hosts):
  (fd, filename) = tempfile.mkstemp(prefix='hosts-', dir=os.path.abspath('.'))
  for host in bad_hosts:
    os.write(fd, host + lf)
  os.close(fd)
  return filename

def write_to_etc_hosts(host_list):
  etc_hosts = open('/etc/hosts', 'a')
  bad_hosts = open(host_list, 'r')
  data = bad_hosts.read()
  bad_hosts.close()
  etc_hosts.write('# adhostblocker\n' + data)
  etc_hosts.close()

def reset_etc_hosts():
  etc_hosts = open('/etc/hosts', 'r')
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
    etc_hosts = open('/etc/hosts', 'w')
    for line in keep:
      etc_hosts.write(line + lf)
    etc_hosts.close()

def main():
  bad = get_blacklist()
  host_list = save_hosts(bad)
  reset_etc_hosts()
  write_to_etc_hosts(host_list)

if __name__ == '__main__':
  main()
