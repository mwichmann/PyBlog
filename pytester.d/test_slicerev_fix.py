import pytest
from reverser import slicerev

@pytest.fixture(params=[
    ([1,2,3,4], [4,3,2,1]),
    ((1,2,3,4), (4,3,2,1)),
    ('abcd',    'dcba')
    ])
def slicedata(request):
    return request.param

def test_slicerev(slicedata):
    input, expected = slicedata
    output = slicerev(input)
    assert output == expected
