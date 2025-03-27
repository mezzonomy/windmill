from solver import TileSolver, Periodicity

from flask import Flask, request, send_from_directory, jsonify
import os
app = Flask(__name__, static_folder='static')

# Route pour servir le fichier HTML principal
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Route pour le solver SAT sur un rectangle (x,y) avec description lst
@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    x = int(data.get('x'))
    y = int(data.get('y'))
    lst    = data.get('liste')     
    solver = TileSolver(x, y, tiles = lst)
    model  = solver.solve()
    return jsonify({'N':solver.N, 'w':solver.wang_tiles, 's':solver.format_solution(model)})

# Route pour vérifier l'existence de rectangles périodiques
@app.route('/period', methods=['POST'])
def period():
    data = request.get_json()
    N = int(data.get('N'))
    w = data.get('w')
    s = data.get('s')
    period = Periodicity(N, w, s)
    return jsonify(period.all())

# Pour servir tous les autres fichiers statiques (JS, CSS, images, etc.)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True) 
