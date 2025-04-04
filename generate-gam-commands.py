#!/usr/bin/python3
#Python 3.8.9

# generate commands to run through GAM
# to make a Google Workspace match an alias file

# does not actually run the commands, so they can be sanity checked first

# usage: generate-gam-commands <alias-filename> <domain>

# example: generate-gam-commands /etc/aliases example.com

import sys

aliasfilename = sys.argv[1]
domain = "@" + sys.argv[2]

# 1. parse alias file
forwards = dict(())
groups = dict(())
aliases = dict(())
aliasfile = open(aliasfilename)
for line in aliasfile:
  tokens = [address.rstrip(',') for address in line.split()]
  if tokens[0].endswith(domain):
    key = tokens[0][0:-len(domain)]
    if len(tokens) > 2:
      groups[key] = tokens[1:]
    elif tokens[1].endswith(domain):
      aliases[key] = tokens[1]
    else:
      forwards[key] = tokens[1] 
  else:
    print("# ERROR aliasfile contains entry not for domain:", tokens[0])

# 3. new non-archived groups (forwards) to create
for key, value in forwards.items():
  print("gam create group", key, "name \"", end="")
  print(key.replace("-", " ").title(), "Personal Forward\" isArchived false")
  print("gam update group", key, "add", value)
  
# 4. new archived groups (groups) to create
for key, values in groups.items():
  print("gam create group", key, "name \"", end="")
  print(key.replace("-", " ").title(), "Group Forward\" isArchived true")
  # print(key.replace("-", " ").title(),
  #       "Shared Inbox\" isArchived true enableCollaborativeInbox true")
  for value in values:
    print("gam update group", key, "add", value)

# 5. (local) aliases to create
for key, value in aliases.items():
  val = value[0:-len(domain)] if value.endswith(domain) else value
  if val in forwards.keys() or val in groups.keys():
    print("gam create alias", key, "group", val)
  else:
    print("gam create group", key, "name \"", end="")
    print(key.replace("-", " ").title(), "Forward\" isArchived false")
    print("gam update group", key, "add", value)
