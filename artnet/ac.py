for shift in range(0,48,8):
    start_points = range(shift,shift+8)
    for index, letter in enumerate("abcdef"):
        mapping = list(map(lambda x: (x+1+(index*8))%48, start_points))
        print(letter, mapping)
