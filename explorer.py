palette   = "mMnNo"

from itertools import product, permutations
length    = 8 # square windmill

windmills = []
scans     = {}
build     = lambda t,p : ''.join([palette[p[t[i]]] for i in range(len(t))])
colors    = tuple(range(len(palette)))
for t in product(colors, repeat = length): 
    for p in permutations(colors):
        ppt = build(t,p)
        if p==colors:
            if ppt in scans: 
                break
            windmills.append(ppt)
        for rotation in range(4):
            scans[ppt] = None
            if False: scans[pt[::-1]] = None
            ppt =  ppt[2:] + ppt[:2] 

from solver import TileSolver, Periodicity
for size in range(2, 20):
    cardinal = len(windmills)
    locked = 0
    periodic = 0
    for windmill in windmills:
        solver = TileSolver(size, size, [windmill])
        model  = solver.solve()
        if not model:
            locked += 1
            windmills.remove(windmill)
            continue
        periods = Periodicity(solver.N, solver.wang_tiles, solver.format_solution(model))
        if periods:
            periodic += 1
            windmills.remove(windmill)
    print(f'Size {size}, Still {cardinal}, and {locked} with no solution, and {periodic} periodic')

print(windmills)
cardinal = len(windmills)
print(f'Size {size} give {cardinal} candidates')

