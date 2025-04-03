from pysat.solvers import Solver
from pysat.formula import CNF
from itertools import product

# Periodicity check
class Periodicity:

    def pos_var(self, idx):
        if idx < 1:
            raise ValueError("Index must be greater than or equal to 1")
        t_idx = idx - 1
        combined = (idx - 1) // len(self.wang_tiles)
        i = combined % self.N
        j = combined // self.N
        return i, j, t_idx % len(self.wang_tiles)

    def __init__(self, N, wang_tiles, sol):
        self.N          = N
        self.wang_tiles = wang_tiles
        self.sol        = sol
        self.M          = max([self.pos_var(s)[1] + 1 for s in self.sol])
        self.matrix     = [ (['']*self.N)[:] for _ in range(self.M)]
        #print(self.N, self.M, self.matrix)
        for s in self.sol:
            i,j,it = self.pos_var(s)
            try:
                self.matrix[j][i] = self.wang_tiles[it]
            except:
                print(i,j,it)
        #print(self.matrix)

    def CheckTile(self, x0, y0, x1, y1):
        try:
            top    = ''.join([self.matrix[y0][ x][0:2]       for x in range(x0, x1+1)])
            right  = ''.join([self.matrix[ y][x1][2:4]       for y in range(y0, y1+1)])
            bottom = ''.join([self.matrix[y1][ x][4:6][::-1] for x in range(x0, x1+1)])
            left   = ''.join([self.matrix[ y][x0][6:8][::-1] for y in range(y0, y1+1)])
        except:
            raise Exception(self.N, self.M, x0, y0, x1, y1)
        test   = top == bottom and left == right
        #if test: print((x0, y0,  x1+1, y1+1), ":", (top, right, bottom, left))
        return test

    def all(self):
        response = []
        for w, h in product(range(1, self.N + 1), range(1, self.M + 1)):
            for x, y in product(range(self.N - w), range(self.M - h)):
                if self.CheckTile(x, y, x + w, y + h):
                    response.append([x, y, x + w + 1, y + h + 1])
        return response

    def has(self):
        for w, h in product(range(1, self.N + 1), range(1, self.M + 1)):
            for x, y in product(range(self.N - w), range(self.M - h)):
                if self.CheckTile(x, y, x + w, y + h):
                    return True
        return False

    def overlap(self, ex, tile):
        [x11, y11, x12, y12] = ex
        [x21, y21, x22, y22] = tile
        # Check for no overlap along the x-axis
        if x12 <= x21 or x22 <= x11:
            return False
        # Check for no overlap along the y-axis
        if y12 <= y21 or y22 <= y11:
            return False
        return True 


    def overlaps(self,response, tile):
        for ex in response:
            if self.overlap(ex, tile):
                return True
        return False

    def distincts(self):
        response = []
        for w, h in product(range(1, self.N + 1), range(1, self.M + 1)):
            for x, y in product(range(self.N - w), range(self.M - h)):
                if self.CheckTile(x, y, x + w, y + h):
                    tile = [x, y, x + w + 1, y + h + 1]
                    if not(self.overlaps(response, tile)):
                        response.append(tile)
        return response

# SAT solver for windmill
class TileSolver:
    def __init__(self, x, y, tiles = ['owjwjwow', 'woRBwoRB', 'owjoRBww',
            'owojRBkw', 'BRBRBRBR', 'wwojBBLB', 'wkojBBBL', 'wjBBBRBL', 'woBBBRLB']):
        """Initialisation du solveur et des paramètres"""
        self.N, self.M = x,y  # Taille de la grille
        #self.N, self.M = 2, 2  # DEBUG
        self.cnf = CNF()

        # Définition des tuiles avec rotations
        self.wang_tiles, self.desc = self.generate_wang_tiles(tiles)

        # Ajout des contraintes
        self.add_tile_constraints()
        self.add_adjacency_constraints()

    def generate_wang_tiles(self, tiles):
        """Génère les tuiles de Wang avec leurs rotations."""
        wang = []; desc = []; idx = 0
        for tile in tiles:
            idx += 1; rotate = 0
            while not tile in wang:
                wang.append(tile); desc.append((idx, rotate * 90,))
                tile = tile[2:] + tile [:2]; rotate += 1
        #print (wang)
        return wang, desc

    def var_pos(self, i, j, t_idx):
        """Encode une position (i, j) avec l'index de la tuile en variable SAT."""
        return 1 + (i + j*self.N) * len(self.wang_tiles) + t_idx

    def add_tile_constraints(self):
        """Ajoute les contraintes de positionnement des tuiles."""
        for i, j in product(range(self.N), range(self.M)):
            clause = [self.var_pos(i, j, t_idx) for t_idx in range(len(self.wang_tiles))]
            self.cnf.append(clause)

    def add_adjacency_constraints(self):
        """Ajoute les contraintes de correspondance entre tuiles adjacentes."""
        for i, j in product(range(self.N), range(self.M-1)):  
            self.add_constraints_for_neighbors(i, j, i, j+1, 5, 0, 4, 1) # Nord-Sud
        for i, j in product(range(self.N-1), range(self.M)):  
            self.add_constraints_for_neighbors(i, j, i+1, j, 2, 7, 3, 6) # Ouest-Est

    def add_constraints_for_neighbors(self, i1, j1, i2, j2, idx1, idx2, idx3, idx4):
        """Ajoute une contrainte entre deux tuiles adjacentes selon leurs indices."""
        for t1_idx, t2_idx in product(range(len(self.wang_tiles)), repeat=2):
            t1, t2 = self.wang_tiles[t1_idx], self.wang_tiles[t2_idx]
            if (t1[idx1] != t2[idx2] or t1[idx3] != t2[idx4]):
                clause = [-self.var_pos(i1, j1, t1_idx), -self.var_pos(i2, j2, t2_idx)]
                self.cnf.append(clause)

    def solve(self):
        """Exécute le solveur SAT et affiche les solutions."""
        # print(self.cnf.clauses)
        solver = Solver(name='g3', bootstrap_with=self.cnf.clauses)
        solver.solve()
        model = solver.get_model()
        solver.delete()
        return model
        
    def format_solution(self, model):
        """Formate la solution."""
        if model :
            return [idx for idx in model if idx > 0]
        else: 
            return None

    def mp(self):
        model   = self.solve()
        if not model:
            return False, None
        periods = Periodicity(self.N, self.wang_tiles, self.format_solution(model))
        return True, periods.has()


if __name__ == '__main__':
    from sys import argv
    a_set     = argv[-1]
    try:
        SIZE = int(argv[-2])
    except:
        SIZE = 20; 
    windmill = 8
    as_list   = [a_set[i:i + windmill] for i in range(0, len(a_set), windmill)]
    print(TileSolver(SIZE, SIZE, tiles = as_list).mp())
