# ----------------------------------------------------
#   C I T I Z E N   P A R T 

palette   = "mM"
size      = 3

# ----------------------------------------------------
from itertools import product, permutations
from explore import explore, perfmeter

print(size, 'windmills and', f'{len(palette)} color palette:', palette)
# windmill = 6  # triangles 
# windmill = 12 # hexagons 
windmill = 8  # squares

sets    = []; scans   = {}
build   = lambda t,p : ''.join([palette[p[t[i]]] for i in range(len(t))])
colors  = tuple(range(len(palette)))

cardinal = pow(len(colors), windmill * size)
idx      = 0; prop     = 0
for t in product(colors, repeat = windmill * size):
    idx += 1
    progress = 100*idx/cardinal
    prop = perfmeter(progress, cardinal, prop)
    # - 
    for p in permutations(colors):
        ppt = build(t,p)
        if p==colors: # root combination
            if ppt in scans: break
            sets.append(ppt)
        for cmt in permutations(range(size)):
            cppt =''.join([ppt[p*8:(p+1)*8] for p in cmt])
            for rotation in range(pow(4,size)):
                scans[cppt] = None
                for pw in range(size):
                    if (rotation % pow(4,pw)==0):
                        cppt = (
                            cppt[:pw*8] + 
                            cppt[pw*8+2:pw*8+8] + 
                            cppt[pw*8+0:pw*8+2] +  
                            cppt[pw*8+8:]
                        )
print('wrt. rotations: ', cardinal, "sets reduced to", len(sets), "sets")

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
n, sets, last_rats = explore(sets)
cardinal = len(sets)
print(f'After {n}x{n}: it remains {cardinal} candidates')
if sets:
    print(' '.join(sets))
else:
    print('The last rats standing were:', ' '.join(last_rats))
