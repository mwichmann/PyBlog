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

if os.getenv('UPDATE_DEBUG', '0') == '1':
    DEBUG = True
else:
    DEBUG = False


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
    'app' argument used to validate that there is usable data
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

def update_check(app, version=None, cacheupdate=True):
    '''check if 'app' needs updating.

    Cached version is compared against entry in an upstream database.
    If 'version' is supplied, compare that against the upstream version.
    '''
    cache = _yaml_from_cache()

    # Build a default if no usable cache data found
    if not cache or not cache.has_key(app):
        if not cache:
            cache = {}
        if DEBUG:
            print "no cached entry for %s found, building default" % app
        tmpcache = yaml.safe_load(blankapp % (app, '1.0', app))
        cache[app] = tmpcache[app]

    previous = cache[app]
    if version:
        previous['version'] = version
    if DEBUG:
        print "Cache...", yaml.dump(previous, default_flow_style=False)

    # get current version details from update source
    current = _yaml_from_current(app)
    if DEBUG:
        print "From web...", yaml.dump(current[app], default_flow_style=False)

    # save current info for this app to cache
    if cacheupdate:
        cache[app] = current[app]
        with open(UPDATE_CACHE, 'w') as f:
            f.write(yaml.dump(cache, default_flow_style=False))

    # check for version change
    # TODO: "not equal" is not the best test, pull in version-compare code
    oldvers = previous['version']
    newvers = current[app]['version']
    if oldvers != newvers:
        if DEBUG:
            print "version change detected: %s -> %s" % (oldvers, newvers)
        return current[app]['url']
    else:
        if DEBUG:
            print "version has not changed (is: %s)" % oldvers
        return None


if __name__ == "__main__":
    # For testing, use these:
    testversion = "0.0"
    UPDATE_CACHE = ".testcache.yml"
    DEBUG=True

    # TODO test cases: some combinations of
    # add dummy "upstream"
    # check against no cache
    #   1. correctly fall back to defaults?
    #   2. if write flag supplied, is cache created?
    # check against cache with data but without entry for app
    #   1. correctly fall back to defaults?
    #   2. if write flag, is cache updated preserving other data?
    # check against cache with out of date entry for app (only)
    #   1. if write flag, is cache updated?
    # check against cache with out of date entry for app and other data
    #   1. if write flag, is cache updated preserving other data?
    # check using supplied version 
    #   1. is supplied version used instead of cached?
    # check against new data without entry for app
    # check against new data with app version lower than supplied

    print "checking update vs cache version, do not update cache"
    if update_check("test", cacheupdate=False):
        print "checkupdate: test: update needed"
    else:
        print "checkupdate: test: update not needed"

    print "checking update vs v0.0, update cache"
    if update_check("test", testversion, cacheupdate=True):
        print "checkupdate: test: update needed"
    else:
        print "checkupdate: test: update not needed"
