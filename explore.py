from solver import TileSolver, Periodicity
from itertools import product, permutations, combinations
from datetime import datetime

current = datetime.now()
CONSOLE = "\n" # DEBUG
CONSOLE = "\r"

def stamp():
    now = datetime.now()
    time_interval = now - current
    hours = time_interval.seconds // 3600
    minutes = (time_interval.seconds % 3600) // 60
    seconds = time_interval.seconds % 60
    return f'%  in {hours}h{minutes}\'{seconds}"'

def perfmeter(progress, cardinal, prop):
    if (progress < 1):
        print(' ', cardinal, progress, ' %  ', end="\r")
    else: 
        progress = int(progress)
        if (not prop == progress):
            print(' ', cardinal, progress, stamp(), end=CONSOLE)
            prop = progress
    return prop

def stage_information(n, iteration, locked, periodic, subperiodic):
    print(f'After {n}x{n} over {iteration}:', end=" ")
    if (subperiodic == 0):
        if (locked == 0):
            print(f'{periodic} periodic', stamp())
        else:
            print(f'{locked} locked and {periodic} periodic', stamp())
    else:
        if (locked == 0):
            print(f'{periodic} periodic and {subperiodic} subperiodic', stamp())
        else:
            print(f'{locked} locked, {periodic} periodic and {subperiodic} subperiodic', stamp())                    

chunks  = lambda a_set: [a_set[i:i + 8] for i in range(0, len(a_set), 8)]
build   = lambda t, p, pl : ''.join([pl[p[t[i]]] for i in range(len(t))])
connect = lambda a_set: [a_set[i:i + 2] for i in range(0, len(a_set), 2)]

def isminimum(t, palette, colors, pairs, size):
    # t: sequence of eight colors
    # palette: a string
    # colors = range(len(palette))
    # size = len(t)//8
    assert len(t)%8==0
    plain = tuple([_*2 for _ in palette])
    tile = build(t,colors, palette)
    OVERHEAD = len(colors) < 6
    if OVERHEAD:
        shunt = permutations(colors)
    else:
        shunt = [None]
    for p,c in product(permutations(colors), shunt):
        ppt     = build(t,p, palette)
        if OVERHEAD:
            permut  = dict(zip(palette, [palette[c[_]] for _ in colors]))
            shuffle = dict(zip(pairs + plain, tuple([permut[p[0]]+permut[p[1]] for p in pairs]) + plain))
            ppt     = ''.join([shuffle[ch] for ch in connect(ppt)])
        for cmt in permutations(range(size)):
            cppt =''.join([ppt[p*8:(p+1)*8] for p in cmt])
            for rotation in range(pow(4,size)):
                if cppt < tile: 
                    return False
                for pw in range(size):
                    if (rotation % pow(4,pw)==0):
                        cppt = (
                            cppt[:pw*8] + 
                            cppt[pw*8+2:pw*8+8] + 
                            cppt[pw*8+0:pw*8+2] +  
                            cppt[pw*8+8:]
                        )
    return tile

def normalize(tile):
    palette = [_ for _ in dict([(c, None) for c in tile]).keys()]
    colors  = range(len(palette))
    mapping = dict(zip(palette, colors))
    t       = [mapping[c] for c in tile]
    return minimum(t, palette, colors, len(tile)//8)
    

def explore(sets, cardinal, stage_information = stage_information, perfmeter = perfmeter):
    n = 2
    while True:
        sieve     = [];  # kept sets
        locked    = 0; periodic  = 0; subperiodic = 0; last_rats = [] # outputs
        idx       = 0; prop      = 0                                  # performance
        for a_set in sets:
            if (n>2): # perfmeter in generator
                idx += 1; progress = 100*idx/cardinal
                prop = perfmeter(progress, cardinal, prop)
            as_list = chunks(a_set)
            model, period  = TileSolver(n, n, tiles = as_list).mp()
            if not model:
                locked += 1
                continue
            if period:
                periodic += 1
                last_rats.append(a_set)
                continue
            keep    = True 
            for subsize in range(1,len(as_list)):
                if not(keep):
                    break
                for sublist in combinations(as_list, subsize):
                    model, period  = TileSolver(n, n, tiles = sublist).mp()
                    if not model: 
                        continue
                    if period:
                        keep = False
                        subperiodic += 1
                        break
            if keep:
                sieve.append(a_set)
            # - End sieve for a_set at a given size
        if (periodic == 0 and locked==0 and subperiodic == 0):
            break
        stage_information(n, idx, locked, periodic, subperiodic)
        if len(sieve)==0:
            break
        n += 1
        sets = sieve
        cardinal = len(sets)
        # - End loop
    return n, sieve, last_rats

def develop(sets, cardinal, stage_information = stage_information, perfmeter = perfmeter):
    n = 2
    unperiodic = [];  # cumulative kept sets
    while True:
        sieve      = [];  # kept sets
        locked = 0; periodic  = 0; subperiodic = 0; # outputs
        idx    = 0; prop      = 0                                  # performance
        for a_set in sets:
            if (n>2): # perfmeter in generator
                idx += 1; progress = 100*idx/cardinal
                prop = perfmeter(progress, cardinal, prop)
            as_list = chunks(a_set)
            model, period  = TileSolver(n, n, tiles = as_list).mp()
            if not model:
                locked += 1
                unperiodic.append(a_set)
                continue
            if period:
                periodic += 1
                continue
            keep    = True 
            for subsize in range(1,len(as_list)):
                if not(keep):
                    break
                for sublist in combinations(as_list, subsize):
                    model, period  = TileSolver(n, n, tiles = sublist).mp()
                    if not model: 
                        continue
                    if period:
                        keep = False
                        subperiodic += 1
                        break
            if keep:
                sieve.append(a_set)
            # - End sieve for a_set at a given size
        if (periodic == 0 and locked==0 and subperiodic == 0):
            break
        stage_information(n, idx, locked, periodic, subperiodic)
        if len(sieve)==0:
            break
        n += 1
        sets = sieve
        cardinal = len(sets)
        # - End loop
    print('develop', len(sieve), len(unperiodic))
    return n, sieve + unperiodic

if __name__ == '__main__':
    from sys import argv
    print(normalize(argv[-1]))

# owjwjwowwoRBwoRBowjoRBwwowojRBxwBRBRBRBRwwojBBABwxojBBBAwjBBBRBAwoBBBRAB
