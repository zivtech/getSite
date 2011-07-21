#!/usr/bin/env python

# Import the necessary libraries
import sys
import httplib, urllib
import urllib2
#import json
import simplejson

siteURL = ''
APIKey = ''

def setCredentials(url, key):
  global siteURL
  global APIKey
  siteURL = url
  APIKey = key

# Get a site by its unique name
def getSiteByName(name=''):
  sites = getAllSites()
  if name in sites:
    return {
      'status' : 'success',
      'data' : sites[name]
    }
  else:
    return {
      'status' : 'error',
      'message' : 'You typed in the wrong site name or one that does not exist.'
    }

# Get all sites
def getAllSites():
  # Get raw site data
  sites = getAllSitesData()
  # Set default values
  defaults = {
    # (Required) The name of the client for whom this site is maintained.
    # 'client' : 'zivtech',
    # The path to the remote repository.
    #(Required) 'repository' : 'https://zivtech.unfuddle.com/svn/zivtech_dahon',
    # The ssh alias for the host this site is hosted on.
    # Optional, defaults to site lisa (our dev server).
    'host' : 'lisa',           
    # Optional, defaults to host. The PHP head (or heads) where the site is hosted.
    # 'code hosts' : "{'lisa'}"
    # Optional, defaults to host.  The server where the files are stored 
    # (may be an NFS server on large sites).
    # 'files host' : 'lisa',
    # Optional, defaults to site name key.  The MySQL server for the site.
    # 'mysql host' : 'lisa',
    # Number of times to run cron per hour.  Optional, defaults to 1.
    'cron_frequency' : 1,      
    # Optional, defaults to site name key. The path to the MySQL host
    # 'webroot' : 'dahon-dev',   
    # Optional, specify the VCS used for this site.
    # Currently supports svn and git.
    'vcs' : 'svn',             
    # Optional, specify the major Drupal version used for this site.
    # Currently supports D6 and D7.
    'version' : 'D7',
    # Optional, specify if this site uses private files.
    # Default is no.
    'private files' : False,
  }
  for siteName, siteData in sites.iteritems(): 
    for name, value in defaults.iteritems():
      if name not in siteData:
        sites[siteName][name] = value
    if 'code hosts' not in siteData:
      sites[siteName]['code hosts'] = sites[siteName]['host']
    if 'files host' not in siteData:
      sites[siteName]['files host'] = sites[siteName]['host']
    if 'mysql host' not in siteData:
      sites[siteName]['mysql host'] = sites[siteName]['host']
    if 'webroot' not in siteData:
      sites[siteName]['webroot'] = siteName
  return sites

def getAllSitesData():
  # Retreve sites from extranet service
  global APIKey
  global siteURL
  params = urllib.urlencode({'api_key': APIKey})
  response = urllib2.urlopen(siteURL, params)
  sites = simplejson.load(response)
  response.close()
  return sites

def getSitesForHost(hostname, type=''):
  """Return site data for all sites on a given host."""
  if type == '':
    type = 'files host'

  sites = getAllSites()
  hostSites = {}
  for siteName, siteData in sites.iteritems(): 
    if siteData[type] == hostname:
      hostSites[siteName] = siteData
  return hostSites

def getThisHostname():
  file = open('/etc/hostname')
  hostname = file.read().strip()
  file.close
  return hostname
  
def getSitesForThisHost(type=''):
  hostname = getThisHostname()
  return getSitesForHost(hostname, type)

