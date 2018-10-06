from reverser import slicerev


def test_slicerev_list():
    output = slicerev([1, 2, 3, 4])
    assert output == [4, 3, 2, 1]


def test_slicerev_tuple():
    output = slicerev((1, 2, 3, 4))
    assert output == (4, 3, 2, 1)


def test_slicerev_string():
    output = slicerev('abcd')
    assert output == 'dcba'
