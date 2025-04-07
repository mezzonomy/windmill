# ----------------------------------------------------
#   C I T I Z E N   P A R T 
from sys import argv
palette   = argv[-1]
size      = int(argv[-2])

# ----------------------------------------------------
from itertools import product, permutations, combinations
from explore import explore, perfmeter, isminimum

# windmill = 6  # triangles 
# windmill = 12 # hexagons 
# windmill = 8  # squares (& kites)

colors  = tuple(range(len(palette)))
cardinal = pow(len(colors), 8 * size)

def generate(size):
    print(size, 'windmills and', f'{len(palette)} color palette: {cardinal} checks')
    idx      = 0; prop     = 0;
    pairs    = [''.join(_) for _ in combinations(palette, 2)]+[''.join(_[::-1]) for _ in combinations(palette, 2)]
    for t in product(colors, repeat = 8 * size):
        idx += 1; progress = 100*idx/cardinal
        prop = perfmeter(progress, cardinal, prop)
        # - 
        a = isminimum(t, palette, colors, tuple(pairs), size)
        if a: yield a

# print('wrt. rotations: ', cardinal, "sets reduced to", len(sets), "sets")

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
n, sets, last_rats = explore(generate(size), cardinal)
cardinal = len(sets)
print(f'After {n}x{n}: it remains {cardinal} candidates')
if sets:
    print(' '.join(sets))
else:
    print('The last rats standing were:', ' '.join(last_rats))
