#!/usr/bin/python
''' checkupdate: check if a given script has been updated

Retrieves a yaml-format update file and compares the entry for
the given script name with a cached one
'''

__all__ = ["update_check"]

import os
import yaml
import requests
from distutils.version import StrictVersion

PROGRAMNAME = 'checkupdate'
PROGRAMVERSION = '0.3'
DEFAULT_UPDATE_SOURCE = 'https://raw.github.com/mwichmann/PyBlog/master/updater.d/update-log.yml'
DEFAULT_UPDATE_CACHE = os.path.expanduser('~' + '/.version_cache.yml')


def _setup_environ():
    global UPDATE_SOURCE, UPDATE_CACHE, DEBUG

    # get variables from environment, defaulting if not set
    UPDATE_SOURCE = os.getenv('UPDATE_SOURCE', DEFAULT_UPDATE_SOURCE)
    UPDATE_CACHE = os.getenv('UPDATE_CACHE', DEFAULT_UPDATE_CACHE)

    if os.getenv('UPDATE_DEBUG', '0') == '1':
        DEBUG = True
    else:
        DEBUG = False


def _yaml_from_cache(app):
    '''load a previous update check from cache
    If there is no cache, or a valid entry is not found, build
    something to return anyway.
    '''
    # load previous check results from cache
    cache_yaml = None
    if os.path.isfile(UPDATE_CACHE):
        with open(UPDATE_CACHE, 'r') as cachefile:
            cache_yaml = yaml.safe_load(cachefile)
            if DEBUG:
                if cache_yaml:
                    print "read cache file %s" % UPDATE_CACHE
                else:
                    print "cache file contents invalid, skipping"

    # Build a default if no usable cache data found
    if not cache_yaml or not cache_yaml.has_key(app):
        if not cache_yaml:
            cache_yaml = {}
        if DEBUG:
            print "no cached entry for %s found, building default" % app
        entry = {
            'name': app,
            'sha256': '',
            'releasedate': '',
            'version': '0.0',
            'url': ''
        }
        cache_yaml[app] = entry

    return cache_yaml


def _yaml_from_current(app):
    '''get current version details from update source
    We assume get + load yaml will leave None if something went wrong.
    'app' argument used to validate that there is usable data
    If the function returns, we are good to proceed.
    '''

    # requests cannot handile file://, so fudge it
    if UPDATE_SOURCE.startswith('file://'):
        fname = UPDATE_SOURCE.split('file://')[1]
        with open(fname, 'r') as updatefile:
            current_yaml = yaml.safe_load(updatefile)
    else:
        reqdata = requests.get(UPDATE_SOURCE)
        current_yaml = yaml.safe_load(reqdata.text)

    # Devide if we can use the update data. If not, there is
    # no work to do, so we return none so the API can report that.
    if not current_yaml:
        print "Warning: there is no valid data in the updates source"
        print "check %s is the correct path" % UPDATE_SOURCE

    if not current_yaml.has_key(app):
        print "Warning: there is no entry in the updates source for", app
        print "check validity of %s" % UPDATE_SOURCE
        current_yaml = None

    return current_yaml


def update_check(app, version=None, cacheupdate=True):
    '''check if 'app' needs updating.
    Cached version is compared against entry in an upstream database.
    If optional 'version' is supplied, compare that against the update
    source.  Returns a URL to the update if one is needed, else None.
    '''
    _setup_environ()

    # get cached version details
    cache = _yaml_from_cache(app)
    previous = cache[app]
    if version:
        previous['version'] = version

    # get current version details from update source
    current = _yaml_from_current(app)
    if not current:
        return None

    # if requested, save current info for this app to cache
    if cacheupdate:
        cache[app] = current[app]
        with open(UPDATE_CACHE, 'w') as cachefile:
            cachefile.write(yaml.dump(cache, default_flow_style=False))

    oldvers = previous['version']
    newvers = current[app]['version']
    if StrictVersion(newvers) > StrictVersion(oldvers):
        if DEBUG:
            print "version change detected (%s -> %s)" % (oldvers, newvers)
        return current[app]['url']
    else:
        if DEBUG:
            print "version has not changed (current %s)" % oldvers
        return None


if __name__ == "__main__":
    # if not called as a module, check ourselves
    rv = update_check(PROGRAMNAME, PROGRAMVERSION, cacheupdate=False)
    print PROGRAMNAME, rv
