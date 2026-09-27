import pprint
pp = pprint.PrettyPrinter(indent=4)

for a in range(97, 103):
    for b in range(1, 49):
        print('{:c}{}'.format(a, b))
