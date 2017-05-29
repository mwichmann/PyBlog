''' checkupdate: check if a given script has been updated

Retrieves a yaml-format update file and compares the entry for
the given script name with a cached one
'''

import requests
import yaml
import re
import os
import sys

# this is a template entry, used if we have no previous information
blankapp = '''
    %s:
        url: ''
        sha256: ''
        releasedate: ''
        version: '%s'
        name: '%s'
'''

# get variables from environment, defaulting if not set
DEFAULT_UPDATE_SOURCE = 'https://raw.github.com/mwichmann/PyBlog/master/updater.d/update-log.yml'
DEFAULT_UPDATE_CACHE = os.path.expanduser('~' + '/.version_cache.yml')
UPDATE_SOURCE = os.getenv('UPDATE_SOURCE', DEFAULT_UPDATE_SOURCE)
UPDATE_CACHE = os.getenv('UPDATE_CACHE', DEFAULT_UPDATE_CACHE)

#if os.getenv('UPDATE_DEBUG', '0') == '1':
#    DEBUG = True
#else:
#    DEBUG = False
DEBUG=True


def _yaml_from_cache():
    '''load a previous update check from cache'''
    # load previous check results from cache
    cache = None
    if os.path.isfile(UPDATE_CACHE):
        if DEBUG:
            print "reading cache file %s" % UPDATE_CACHE
        with open(UPDATE_CACHE, 'r') as f:
            cache = yaml.safe_load(f)
        if not cache:
            if DEBUG:
                print "cache file contents invalid, skipping"

    return cache


def _yaml_from_current(app):
    '''get current version details from update source

    We assume get + load yaml will leave None if something went wrong
    'app' argument is use to validate that the fetched data actually
    is usable. 
    If the function returns, we are good to proceed.
    '''
    r = requests.get(UPDATE_SOURCE)
    current_yaml = yaml.safe_load(r.text)
    if not current_yaml:
        print "Fatal: there is no valid data in the updates source"
        print "check %s is the correct path" % UPDATE_SOURCE
        os.exit(1)

    if not current_yaml[app]:
        print "Fatal: there is no entry in the updates source for", app
        print "check validity of %s" % UPDATE_SOURCE
        os.exit(1)

    return current_yaml


def _yaml_print_entry(yml):
    '''print an app entry (for debugging purposes'''
    yaml.dump(yml)

def update_check(app, version=None):
    '''check if 'app' needs updating.

    Cached version is compared against entry in an upstream database.
    If 'version' is supplied, compare that against the upstream version.
    '''
    cache = _yaml_from_cache()

    # select the previous entry for "app", or build a default if not found
    if not cache or not cache[app]:
        if DEBUG:
            print "using default app template, no cache entry"
        if not version:
            version = '0.0'
        #previous = yaml.safe_load(blankapp % (app, version, app))
        cache = yaml.safe_load(blankapp % (app, version, app))
    previous = cache[app]
    if version:
        previous['version'] = version
    if DEBUG:
        #print yaml.dump(cache)
        print yaml.dump(previous)

    # get current version details from update source
    current = _yaml_from_current(app)
    if DEBUG:
        #print yaml.dump(current)
        print yaml.dump(current[app])

    # save current version to cache
    # TODO: we really only want to merge in current entry for 'app',
    # else cache could indicate a different app had been updated
    # when no check has beeen made. Currently, cheap way: just dump
    # the whole current yaml out to the cache.
    with open(UPDATE_CACHE, 'w') as f:
        f.write(yaml.dump(current, default_flow_style=False))

    # check for version change
    oldvers = previous['version']
    newvers = current[app]['version']
    if oldvers != newvers:
        if DEBUG:
            print "version change detected: %s -> %s" % (oldvers, newvers)
        return True
    else:
        if DEBUG:
            print "version has not changed (is: %s)" % oldvers
        return False


if __name__ == "__main__":
    testversion = "0.0"
    if update_check("test", testversion):
        print "checkupdate: test: update needed"
    else:
        print "checkupdate: test: update not needed"
