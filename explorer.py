# ----------------------------------------------------
#   C I T I Z E N   P A R T 

palette   = "mM"
size      = 1

# ----------------------------------------------------

from itertools import product, permutations
windmill = 6  # triangles 
windmill = 12 # hexagons 
windmill = 8  # squares


sets    = []
scans   = {}
build   = lambda t,p : ''.join([palette[p[t[i]]] for i in range(len(t))])
colors  = tuple(range(len(palette)))

cardinal = pow(len(colors), windmill * size)
idx      = 0
prop     = 0
for t in product(colors, repeat = windmill * size):
    # - Perfmeter
    idx += 1
    progress = 100*idx/cardinal
    if (progress < 1):
        print(' ', cardinal, progress, ' %  ', end="\r")
    else: 
        progress = int(progress)
        if (not prop == progress):
            print(' ', cardinal, progress,"%                 ", end="\r")
            prop = progress
    # - Perfmeter
    for p in permutations(colors):
        ppt = build(t,p)
        if p==colors:
            if ppt in scans: 
                break
            sets.append(ppt)
        for rotation in range(pow(4,size)):
            scans[ppt] = None
            for pw in range(size):
                if (rotation % pow(4,pw)==0):
                    ppt = ppt[:pw*4] + ppt[pw*4+2:pw*4+8] + ppt[pw*4+0:pw*4+2] +  ppt[pw*4+8:]
print()
from solver import TileSolver, Periodicity
for n in range(2, 20):
    cardinal = len(sets)
    locked = 0
    periodic = 0
    idx = 0
    prop     = 0
    for a_set in sets:
        # - Perfmeter
        idx += 1
        progress = 100*idx/cardinal
        if (progress < 1):
            print(' ', cardinal, progress, ' %  ', end="\r")
        else: 
            progress = int(progress)
            if (not prop == progress):
                print(' ', cardinal, progress,"%  ", end="\r")
                prop = progress
        # - Perfmeter
        solver = TileSolver(n, n, 
            [a_set[i:i + windmill] for i in range(0, len(a_set), windmill)])
        model  = solver.solve()
        if not model:
            locked += 1
            sets.remove(a_set)
            continue
        periods = Periodicity(solver.N, solver.wang_tiles, solver.format_solution(model))
        if periods:
            periodic += 1
            sets.remove(a_set)
    print(f'Size {n}, Still {cardinal}, and {locked} with no solution, and {periodic} periodic')

print(sets)
cardinal = len(sets)
print(f'Size {n} give {cardinal} candidates')

