
def engine(previous, countdown):
    print('engine', len(previous))
    cardinal = len(previous) * power
    print(f'Stage {countdown} : {cardinal} checks')
    idx      = 0; prop     = 0;
    pairs    = (
        [''.join(_) for _ in combinations(palette, 2)]
        +[''.join(_[::-1]) for _ in combinations(palette, 2)])
    for p,f in product(previous, fuel):
        idx += 1; progress = 100*idx/cardinal
        prop = perfmeter(progress, cardinal, prop)
        # - 
        candidate = p + f
        result = isminimum(candidate, palette, colors, tuple(pairs), countdown)
        if result:
            yield result

# ----------------------------------------------------

from sys import argv
palette = argv[-1]
size    = int(argv[-2])
colors  = tuple(range(len(palette)))
#  6  : triangles 
#  8  : squares  <--- YOU ARE HERE (& kites also)
# 12  : hexagons
# ----------------------------------------------------

from itertools import product, permutations, combinations
from explore import develop, explore, perfmeter, isminimum

fuel    = [_ for _ in product(colors, repeat = 8)]
power   = pow(len(colors), 8) 
print(f'{len(palette)} color palette gives {power} fuel: ')

space = [()]
joint = dict(zip(palette, colors))
for countdown in range(1, size):
    n, nonsolutions = develop(engine(space, countdown), len(space) * power)
    space = [tuple([joint[_] for _ in ns]) for ns in nonsolutions]

n, solutions, periodics = explore(engine(space, size), len(space) * power)

# ----------------------------------------------------

cardinal = len(solutions)
print(f'After {n}x{n}: it remains {cardinal} candidates')
if solutions:
    print(' '.join(solutions))
else:
    print('The last periodics were:', ' '.join(periodics))
