from solver import TileSolver, Periodicity
from itertools import product, permutations, combinations

def perfmeter(progress, cardinal, prop):
    if (progress < 1):
        print(' ', cardinal, progress, ' %  ', end="\r")
    else: 
        progress = int(progress)
        if (not prop == progress):
            print(' ', cardinal, progress,"%                      ", end="\r")
            prop = progress
    return prop

def stage_information(n, locked, periodic, subperiodic):
    print(f'After {n}x{n}:', end=" ")
    if (subperiodic == 0):
        if (locked == 0):
            print(f'{periodic} periodic')
        else:
            print(f'{locked} locked and {periodic} periodic')
    else:
        if (locked == 0):
            print(f'{periodic} periodic and {subperiodic} subperiodic')
        else:
            print(f'{locked} locked, {periodic} periodic and {subperiodic} subperiodic')                    

def explore(sets, windmill = 8, stage_information = stage_information, perfmeter = perfmeter):
    n = 2
    while True:
        sieve     = [];  # kept sets
        locked    = 0; periodic  = 0; subperiodic = 0; last_rats = [] # outputs
        idx       = 0; prop      = 0                                  # performance
        cardinal = len(sets)
        for a_set in sets:
            idx += 1; progress = 100*idx/cardinal
            prop = perfmeter(progress, cardinal, prop)
            # - 
            as_list = [a_set[i:i + windmill] for i in range(0, len(a_set), windmill)]
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
        stage_information(n, locked, periodic, subperiodic)
        if len(sieve)==0:
            break
        n += 1
        sets = sieve
        # - End loop
    
    return n, sieve, last_rats