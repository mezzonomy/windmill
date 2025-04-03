# ----------------------------------------------------
#   C I T I Z E N   P A R T 

palette = "Bw"

I1  = ''.join([
    "mn______",
    "nm______",
])

L1  = ''.join([
    "mn______",
    "nmnm____",
])

T1  = ''.join([
    "mn______",
    "nmnmnm__",
])

pattern = T1
# ----------------------------------------------------
windmill = 6  # triangles 
windmill = 12 # hexagons 
windmill = 8  # squares

print('pattern', pattern, 'check in GUI', pattern.replace('_','B'))
assert len(pattern)%windmill==0, "Pattern must be of length 8, 16, 24, ..."

size = pattern.count('_')
print(size, 'placeholders in pattern and', f'{len(palette)} color palette:', palette)

colors  = tuple(range(len(palette)))

cardinal = pow(len(colors), size)

sets    = []
for subst in product(colors, repeat = size):
    # - Perfmeter
    idx += 1
    progress = 100*idx/cardinal
    if (progress < 1):
        print(' ', cardinal, progress, ' %  ', end="\r")
    else: 
        progress = int(progress)
        if (not prop == progress):
            print(' ', cardinal, progress,"%                  ", end="\r")
            prop = progress
    # - Perfmeter
    tile = pattern
    for _ in subst:
        tile = tile.replace('_',palette[_], 1)
    sets.append(tile)
    
print("Pattern expanded to", len(sets), "sets")

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
from explore import explore
sets, last_rats = explore(sets)
cardinal = len(sets)
print(f'It remains {cardinal} candidates')
if sets:
    print(' '.join(sets))
else:
    print('The last rats standing were:', ' '.join(last_rats))