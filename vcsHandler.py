# @File
#  Provides a level of abstraction for our VCS related scripts
#  allowing them to work with multiple VCS with relative transparency.

import os
import subprocess

def updateFromUpstream(hostVCS, clientVCS, localDirectory, remoteRepository, verbose): 
  if (hostVCS == 'svn' and clientVCS == 'git'):
    # pull in changes from tracked svn repo
    update = "cd %s; git svn rebase" % (localDirectory)
  elif (hostVCS == 'svn'):
    # update folder from svn
    update = "svn up %s" % (localDirectory)
  elif (hostVCS == 'git'):
    # update folder from git
    update = "cd %s; git pull" % (localDirectory)

  # perform the operation
  subprocess.call(update, shell=verbose)

# @param hostVCS
#   
# @param clientVCS
#   
# @param localDirectory
#   
# @param remoteRepository
#   
# @param label type.
#   Must by branch, or tag.
#
# @param label
#   The branch, tag, etc. to checkout, tag, etc. to checkout
# 
# @param verbose
#   
def checkoutFromUpstream(hostVCS, clientVCS, localDirectory, remoteRepository, verbose, label = ''):
  
  # Provide intelligent defaults for the label to use.
  if (hostVCS == 'svn' and label == ''):
    label = 'trunk'
  elif (hostVCS == 'git' and label == ''):
    label = 'master'

  # If the hostVCS is svn, build the path to the repository.
  if (hostVCS == 'svn'):
    # If the label is trunk in an svn repository, get that folder.
    if label == 'trunk':
      remoteRepository = remoteRepository + '/trunk'
    # Otherwise, if the label has a .x in its name, it's one of our branches so check it out. 
    elif (label):
      remoteRepository = remoteRepository + '/branches/' + label
    else:
      # Otherwise we're checkout out one of our tags.
      remoteRepository = remoteRepository + '/tags/' + label

    # If the host is svn and client is git, use the bridge to pull in the tracked repo.
    if (clientVCS == 'git'):
      checkout = "git svn clone %s %s" % (remoteRepository, localDirectory)
    # If the user hasn't forced use of the git bridge, checkout the code from svn.
    else:
      checkout = "svn co %s %s" % (remoteRepository, localDirectory)
    # Shell out to perform the operation
    try:
      subprocess.call(checkout, shell=verbose)
    except:
      print "There was a problem checkout out the repository.  Do you have access to %s?" % remoteRepository
  # If the host is vcs, clone the repository and checkout the appropriate label
  elif (hostVCS == 'git'):
    clone = "git clone --recursive %s %s " % (remoteRepository, localDirectory)
    subprocess.call(clone, shell=verbose)
    os.chdir(localDirectory)
    if (label == 'master'):
      checkout = "git checkout %s" % (label)
    else:
      checkout = "git checkout --track -b %s origin/%s" % (label, label)

    try:
      subprocess.call(checkout, shell=verbose)
    except:
      print "There was a problem checkout out the repository.  Do you have access to %s?" % remoteRepository
