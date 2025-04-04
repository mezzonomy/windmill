from solver import TileSolver, Periodicity
from itertools import product, permutations, combinations
from datetime import datetime

current = datetime.now()

def stamp():
    now = datetime.now()
    time_interval = now - current
    hours = time_interval.seconds // 3600
    minutes = (time_interval.seconds % 3600) // 60
    seconds = time_interval.seconds % 60
    return f'%  in {hours}h{minutes}\'{seconds}"'

def perfmeter(progress, cardinal, prop):
    # if (progress < 1):
    #     print(' ', cardinal, progress, ' %  ', end="\r")
    # else: 
    if True:
        progress = int(progress)
        if (not prop == progress):
            print(' ', cardinal, progress, stamp(), end="\r")
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

chunks = lambda a_set: [a_set[i:i + 8] for i in range(0, len(a_set), 8)]
build  = lambda t, p, pl : ''.join([pl[p[t[i]]] for i in range(len(t))])

def isminimum(t, palette, colors, size):
    # t: sequence of eight colors
    # palette: a string
    # colors = range(len(palette))
    # size = len(t)//8
    assert len(t)%8==0
    tile = build(t,colors, palette)
    for p in permutations(colors):
        ppt = build(t,p, palette)
        for cmt in permutations(range(size)):
            cppt =''.join([ppt[p*8:(p+1)*8] for p in cmt])
#            cppt = 
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
                for sublist in combinations(as_list, subsize):
                    model, period  = TileSolver(n, n, tiles = sublist).mp()
                    if not model: 
                        continue
                    if period:
                        keep = False; subperiodic += 1
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

if __name__ == '__main__':
    from sys import argv
    print(normalize(argv[-1]))

# owjwjwowwoRBwoRBowjoRBwwowojRBxwBRBRBRBRwwojBBABwxojBBBAwjBBBRBAwoBBBRAB
