def slicerev(collection):
    return collection[::-1]


if __name__ == "__main__":
    print(slicerev([1, 2, 3, 4]))
    print(slicerev((1, 2, 3, 4)))
    print(slicerev('abcd'))
