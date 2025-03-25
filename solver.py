from pysat.solvers import Solver
from pysat.formula import CNF
from itertools import product

# SAT solver for windmill
class TileSolver:
    def __init__(self, x, y, tiles = ['owjwjwow', 'woRBwoRB', 'owjoRBww',
            'owojRBkw', 'BRBRBRBR', 'wwojBBLB', 'wkojBBBL', 'wjBBBRBL', 'woBBBRLB']):
        """Initialisation du solveur et des paramètres"""
        self.N, self.M = x,y  # Taille de la grille
        #self.N, self.M = 2, 2  # DEBUG
        self.cnf = CNF()

        # Définition des tuiles avec rotations
        self.wang_tiles = self.generate_wang_tiles(tiles)

        # Ajout des contraintes
        self.add_tile_constraints()
        self.add_adjacency_constraints()

    def generate_wang_tiles(self, tiles):
        """Génère les tuiles de Wang avec leurs rotations."""
        wang = []
        for tile in tiles:
            while not tile in wang:
                wang.append(tile)
                tile = tile[2:] + tile [:2]
        #print (wang)
        return wang

    def var_pos(self, i, j, t_idx):
        """Encode une position (i, j) avec l'index de la tuile en variable SAT."""
        return 1 + (i + j*self.N) * len(self.wang_tiles) + t_idx

    def add_tile_constraints(self):
        """Ajoute les contraintes de positionnement des tuiles."""
        for i, j in product(range(self.N), range(self.M)):
            if False and (i == self.X and j == self.X):
                clause = [self.var_pos(self.X, self.X, 0)] # first tile at the middle.
            else:
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
