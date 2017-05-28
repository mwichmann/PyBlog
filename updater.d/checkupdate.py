''' checkupdate: check if a given script has been updated

Retrieves a yaml-format update file and compares the entry for
the given script name with a cached one
'''

import requests
import yaml
import re
import os
import sys

blankapp = '''
    %s:
        url: ''
        sha256: ''
        releasedate: ''
        version: '%s'
        name: '%s'
'''

# get variables from environment, defaulting if not set
UPDATES_SOURCE = os.getenv('UPDATES_SOURCE', 'https://raw.github.com/mwichmann/PyBlog/master/updater.d/update-log.yml')
UPDATES_CACHE = os.getenv('UPDATES_CACHE', os.path.expanduser('~' + '/.version_cache.yml'))

if os.getenv('UPDATES_DEBUG', '0') == '1':
    DEBUG = True
else:
    DEBUG = False

def update_check(app, version):
    cache_file_loaded = False
    # load previous check results from cache
    if os.path.isfile(UPDATES_CACHE):
        if DEBUG: 
            print "found cache file"
        with open(UPDATES_CACHE, 'r') as f:
            cache = yaml.safe_load(f)
            if cache:
                cache_file_loaded = True
            else:
                if DEBUG: 
                    print "cache file contents invalid, forcing update check"
    else:
        if DEBUG: 
            print "no cache file found, forcing update check"

    # select the entry for "app", or default if not found
    if not cache_file_loaded or not cache[app]:
        previous_check = yaml.safe_load(blankapp % (app, version, app))
    else:
        previous_check = cache[app]

    # get current version details from update source
    r = requests.get(UPDATES_SOURCE)
    current_yaml = yaml.safe_load(r.text)
    if not current_yaml:
        print "Fatal: there is no valid data in the updates source"
        os.exit(1)

    if not current_yaml[app]:
        print "Fatal: there is no entry in the updates source for", app
        os.exit(1)

    # save current version to cache
    with open(UPDATES_CACHE, 'w') as f:
        f.write(yaml.dump(current_yaml, default_flow_style=False))

    # check for version change
    if previous_check['version'] != current_yaml[app]['version']:
        output = "version change detected: {} -> {}".format(previous_check['version'], current_yaml[app]['version'])
        return True
        if DEBUG:
            print output
    else:
        if DEBUG:
            print "latest version has not changed (is: {})".format(current_yaml[app]['version'])
        return False

if __name__ == "__main__":
    testversion = "0.0"
    if update_check("test", testversion):
        print "checkupdate: test: update needed"
    else:
        print "checkupdate: test: update not needed"
