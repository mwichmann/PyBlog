def total1(name, *args):
    if args:
        print("%s has total money of Rs %d/- " %(name, sum(args)))
    else:
        print("%s's piggy bank  has no money" %name)

total1("John", 1, 2, 10)


def total2(name, args):
    if args:
        print("%s has total money of Rs %d/- " %(name, sum(args)))
    else:
        print("%s's piggy bank  has no money" %name)

total2("John", (1, 2, 10))


def total3(name=None, args=None):
    if args:
        print("%s has total money of Rs %d/- " %(name, sum(args)))
    else:
        print("%s's piggy bank  has no money" %name)

total3(name="John", args=(1, 2, 10))




