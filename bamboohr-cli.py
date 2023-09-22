#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# pip3 install tabulate --user
#
# https://help.bamboohr.com/s/article/587919
#############################################################################
import requests
import json
import argparse
import sys, os.path
import numpy as np                      # To remove columns in list of list
from http.client import HTTPConnection  # Debug mode
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from tabulate import tabulate
from datetime import date    

api_ver='v1'
api_base_url='https://api.bamboohr.com/api/gateway.php/'

today=date.today().isoformat()
year=date.today().year
#############################################################################
def request( method='GET', resource='' , auth='', headers={}, params='', data='' ):
  # data:   POST, PUT, ...
  # params: GET, ...
  url=api_url+resource
  headers.update({'accept': 'application/json'})
  if (args.verbose) or (args.debug):
    print(url)
    if (args.debug):
      # print statements from `http.client.HTTPConnection` to console/stdout
      HTTPConnection.debuglevel=1
  response=requests.request(
    method,
    api_url+resource,
    auth=auth,
    headers=headers,
    params=params,
    data=data
  )
  if (args.verbose) or (args.debug):
    print('Status code: '+str(response.status_code))
  if (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())

def istype( table ):
  # print('type:'+istype(['1','2']))
  # print('type:'+istype({'1':'1','2':'2'}))
  if isinstance(table, dict):    # French: Dictionnaire (Table de hachage)
    return('dict')
  elif isinstance(table, float): #         Nombre à virgule flottante
    return('float')
  elif isinstance(table, int):   #         Nombre entier
    return('int')
  elif isinstance(table, list):  #         Liste (Tableau)
    return('list')
  elif isinstance(table, str):   #         Chaîne de caractères
    return('str')
  elif isinstance(table, tuple): #         Multiplet
    return('tuple')
  else:
    return('?')

def print_tabulate( table, tablefmt='rounded_outline', stralign='left', showindex=True, sort=False, reverse=False, sortcolumn='', headers='keys', tablefilterkeys=[], tablefilter=[]):
  # Quick and dirty function!
  # tablefmt: 'simple', 'rounded_outline', 'simple_outline', 'github', ...
  # stralign: 'left', 'center', 'right'
  # missingval='?'
  # showindex: True, False, "Iterable"
  # headers: [array], 'firstrow', 'keys' (if dict)
  # disable_numparse=True
  if (args.verbose) or (args.debug):
    print('type:'+istype(table))
  if tablefilterkeys:
    if (args.verbose) or (args.debug):
      print('Tablesfilterkeys:'+str(tablefilterkeys))
    newtable= []
    for key in table:
      if (args.debug):
        print('Key:'+str(key))
      for tablefilterkey in tablefilterkeys:
         key.pop(tablefilterkey,None)
         newtable.append(key)
    tables=newtable
  if tablefilter:
    if (args.verbose) or (args.debug):
      print('Filter'+str(tablefilter))
    if (args.debug):
      print(table)
    if isinstance(table, list):
      table=np.delete(table, tablefilter, axis=1)
    if isinstance(table, dict):
      print('!!!')
      table=table.drop('photoUrl', inplace=True, axis=1)
  if sort: # Didn't find another way for sort! :(
    if not sortcolumn:
      sortcolumn=next(iter(table[0]))
    if (args.verbose) or (args.debug):
      print('Sort:'+sortcolumn)
      print('Reverse:'+str(reverse))
    #sortkey=(lambda item: (item['displayName']))
    sortkey=(lambda item: (item[sortcolumn]))
    if (args.verbose) or (args.debug):
      print('Sortkey:'+str(sortkey))
    if args.noheaders:
      print(tabulate(sorted(table, reverse=reverse, key=sortkey), tablefmt='plain', showindex=showindex, stralign=stralign))
    else:
      print(tabulate(sorted(table, reverse=reverse, key=sortkey), tablefmt=tablefmt, headers=headers, showindex=showindex, stralign=stralign))
  else:
    if args.noheaders:
      print(tabulate(table, tablefmt='plain', showindex=showindex, stralign=stralign))
    else:
      print(tabulate(table, tablefmt=tablefmt, headers=headers, showindex=showindex, stralign=stralign))
#############################################################################
#############################################################################
parser=argparse.ArgumentParser(description='https://github.com/osgpcq/bamboohr-cli-py',
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the credential')
parser.add_argument('--employees',            action='store_true', help='List employees')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--userenable',           action='store_true', help='With --users only active one')
parser.add_argument('--fields',               action='store_true', help='List fields available for the company')
parser.add_argument('--employee',             action='store',      help='Info for one employee ID')
parser.add_argument('--whosout',              action='store_true', help='Who is out')
parser.add_argument('--today',                action='store_true', help='With --whosout, who is out today')
parser.add_argument('--timeoff',              action='store',      help='iTimeoffCalculator need an employee ID')
parser.add_argument('--noheaders',            action='store_true', help='No headers in the output')
parser.add_argument('--debug',                action='store_true', help='Debug')
#parser.add_argument('--verbose',              action='store_true', default=True, help='Verbose')
parser.add_argument('--verbose',              action='store_true', default=False, help='Verbose')
args=parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser=ConfigParser(interpolation=None)
  parser.read(config_file, encoding='utf-8')
  api_key=parser.get('bamboohr', 'api_key_'+args.client)
  api_url=api_base_url+parser.get('bamboohr', 'api_subdomain_'+args.client)+'/'+api_ver+'/'
  auth=HTTPBasicAuth(parser.get('bamboohr', 'api_key_'+args.client), 'x') 
else:
  sys.exit('Configuration file not found!')

if (args.whosout):
  # Array of dictionary
  whosout=request( resource='time_off/whos_out/', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  if (args.debug):
    print('Sortie request:')
    print(whosout)
  if (args.today):
    if (args.debug):
      print(today)  # '2018-12-05'
  table=[]
  for who in whosout: # List of Dict
    if (args.debug):
      print(who)
    if args.today and (not (who['start'] <= today and today <= who['end'])):
      continue # Pass directly to the next for value
    else:
      table.append(who)
  print_tabulate( table=table, sort=True, sortcolumn='name' )

if (args.employees):
  employees=request( resource='employees/directory', auth=auth, headers={ 'Authorization': 'token '+api_key } ) # Could be disabled by companies
  print_tabulate( table=employees['employees'], tablefilterkeys=['workphone', 'photoUrl', 'workPhoneExtension', 'canUploadPhoto'], sort=True, sortcolumn='displayName' )
if (args.fields):
  fields=request( resource='meta/fields', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  print_tabulate( table=fields )
if (args.users):
  users=request( resource='meta/users', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  table=[]
  for key, values in users.items(): # Dict of List of Dict
    if (args.debug):
      print(key)
      print(values)
    if args.userenable and values['status']=='disabled':
      continue
    else:
      table.append(values)
  print_tabulate( table=table, sort=True ) # sort still now great if in some row, the column is not set
if (args.employee): # Limited access: %2C=',' %20=' '
  # The special employee ID of zero (0) means to use the employee ID associated with the API key (if any)
  #employee=request( resource='employees/0?fields=firstName%2ClastName%2ChireDate&onlyCurrent=true', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  employee=request( resource='employees/'+args.employee+'?fields=firstName%2ClastName%2ChireDate&onlyCurrent=true', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  print_tabulate( table=[employee], showindex=False ) # var passed in list
if (args.timeoff):
  if (args.debug):
    print(year)
  timeoff=request( resource='employees/'+args.timeoff+'/time_off/calculator?end='+str(year)+'-12-31', auth=auth, headers={ 'Authorization': 'token '+api_key } )
  print_tabulate( table=timeoff, showindex=False )
#############################################################################
#############################################################################
#############################################################################
