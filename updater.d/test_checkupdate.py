import pytest
import os
import yaml

# our test target:
from checkupdate import *

TESTAPP = 'test'
TESTVERSION = '0.0'
UPDATE_CACHE = '.testcache.yml'

testentry = {
    'name': TESTAPP,
    'sha256': '',
    'releasedate': '',
    'version': '0.0',
    'url': ''
}
dummyentry =  {
    'name': 'dummy',
    'sha256': '',
    'releasedate': '',
    'version': '0.0',
    'url': ''
}


@pytest.fixture(autouse=True)
def environ(monkeypatch):
    monkeypatch.setenv('TESTAPP', TESTAPP)
    monkeypatch.setenv('UPDATE_CACHE', UPDATE_CACHE)
    #monkeypatch.setenv('UPDATE_DEBUG', '1')
    monkeypatch.setenv('UPDATE_SOURCE', 'file://update-log.yml')


@pytest.fixture
def clean_cache():
    if os.path.exists(UPDATE_CACHE):
        os.remove(UPDATE_CACHE)


@pytest.fixture(params=[
    (False, False),     # cache contains no entries
    (False, True),      # cache contains dummy
    (True, False),      # cache contains test
    (True, True),       # cache contains dummy and test
    ])
def write_cache(request):
    cache = {}
    test, dummy = request.param
    if test:
        cache[TESTAPP] = testentry
    if dummy:
        cache['dummy'] = dummyentry
    with open(UPDATE_CACHE, 'w') as cachefile:
        cachefile.write(yaml.dump(cache, default_flow_style=False))
    return request.param
    

# test each of the cachefile combinations without updating the cache
def test_nocache(clean_cache, write_cache):
    rv = update_check(TESTAPP, cacheupdate=False)
    assert rv == 'file://dummy.py'
    

# now run the combinations so the cache updates, then check again
# second run should report nothing to update
def test_cache(clean_cache, write_cache):
    rv = update_check(TESTAPP, cacheupdate=True)
    assert rv == 'file://dummy.py'
    rv = update_check(TESTAPP, cacheupdate=False)
    assert rv == None

# some more tests to add:
# check using supplied version argument
# - is supplied version used instead of cached?
# validate if updated cache is correct

# Notes on cleanup
'''
# conftest.py
import pytest

@pytest.yield_fixture(autouse=True, scope='session')
def test_suite_cleanup_thing():
    # setup
    yield
    # teardown - put your command here
'''
