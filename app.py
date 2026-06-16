import json
import math
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Global storage for graph configuration
GRAPH_DATA = {}

def load_graph():
    """Safely loads graph dataset from disk on system initialization."""
    global GRAPH_DATA
    json_path = os.path.join(os.path.dirname(__file__), 'graph.json')
    
    if not os.path.exists(json_path):
        json_path = os.path.join(os.path.dirname(__file__), 'old-graph.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
            
            # FORCE STRINGS: Ensures node integer IDs match incoming JavaScript string requests
            GRAPH_DATA['nodes'] = {str(n['id']): n for n in raw_data['nodes']}
            GRAPH_DATA['edges'] = raw_data['edges']
            print(f"✅ SUCCESS: Loaded dataset dynamically from {os.path.basename(json_path)}")
    except Exception as e:
        print(f"⚠️ WARNING: Could not read graph data disk file ({str(e)}). Using fallback Lahore nodes.")
        fallback_data = {
            "nodes": [
                {"id": "1", "name": "Mall Road Hub", "lat": 31.5565, "lon": 74.3262},
                {"id": "2", "name": "Gulberg Central", "lat": 31.5126, "lon": 74.3490},
                {"id": "3", "name": "DHA Phase 3 Hub", "lat": 31.4740, "lon": 74.4010}
            ],
            "edges": [
                {"source": "1", "target": "2", "distance": 6.2, "traffic_factor": 1.4},
                {"source": "2", "target": "3", "distance": 7.8, "traffic_factor": 1.2},
                {"source": "1", "target": "3", "distance": 12.5, "traffic_factor": 1.6}
            ]
        }
        GRAPH_DATA['nodes'] = {str(n['id']): n for n in fallback_data['nodes']}
        GRAPH_DATA['edges'] = fallback_data['edges']

# Initialize data mapping on startup loop
load_graph()


# AI PATHFINDING MODULE: A* SEARCH WITH DYNAMIC TRAFFIC ESTIMATIONS


def haversine_heuristic(node_a_id, node_b_id):
    """Calculates straight-line spatial distance (in km) between positions."""
    nodes = GRAPH_DATA.get('nodes', {})
    if node_a_id not in nodes or node_b_id not in nodes:
        return 0.0
        
    lat1, lon1 = math.radians(nodes[node_a_id]['lat']), math.radians(nodes[node_a_id]['lon'])
    lat2, lon2 = math.radians(nodes[node_b_id]['lat']), math.radians(nodes[node_b_id]['lon'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return c * 6371.0


def a_star_search(start_node, end_node, traffic_mode):
    """AI Pathfinding calculation sequence using real-world coordinates."""
    nodes = GRAPH_DATA.get('nodes', {})
    edges = GRAPH_DATA.get('edges', [])
    
    adjacency_list = {node_id: {} for node_id in nodes}
    for edge in edges:
        u, v = str(edge['source']), str(edge['target'])
        dist = float(edge.get('distance', 1.0))
        
        traffic_multiplier = 1.0
        if traffic_mode == "high":
            traffic_multiplier = float(edge.get('traffic_factor', 1.5))
            
        weight = dist * traffic_multiplier
        if u in adjacency_list: adjacency_list[u][v] = weight
        if v in adjacency_list: adjacency_list[v][u] = weight

    g_score = {node: float('inf') for node in nodes}
    f_score = {node: float('inf') for node in nodes}
    
    g_score[start_node] = 0
    f_score[start_node] = haversine_heuristic(start_node, end_node)
    
    open_set = {start_node}
    previous_nodes = {node: None for node in nodes}
    
    while open_set:
        current_node = min(open_set, key=lambda node: f_score[node])
        if current_node == end_node:
            break
            
        open_set.remove(current_node)
        
        for neighbor, weight in adjacency_list.get(current_node, {}).items():
            tentative_g_score = g_score[current_node] + weight
            if tentative_g_score < g_score[neighbor]:
                previous_nodes[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + haversine_heuristic(neighbor, end_node)
                open_set.add(neighbor)
                
    path = []
    curr = end_node
    while curr is not None:
        path.insert(0, curr)
        curr = previous_nodes[curr]
        
    return path if g_score[end_node] != float('inf') else []

# =====================================================================
# API ROUTING CONTROLLERS
# =====================================================================

@app.route('/')
def home():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: index.html missing from project directory root.", 404

@app.route('/style.css')
def serve_css():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'style.css'), 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/css'}
    except: return "", 404

@app.route('/script.js')
def serve_js():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'script.js'), 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'application/javascript'}
    except: return "", 404

@app.route('/graph.json', methods=['GET'])
def get_graph_json():
    return jsonify({"nodes": list(GRAPH_DATA['nodes'].values()), "edges": GRAPH_DATA['edges']}), 200

@app.route('/shortest_path', methods=['POST'])
def process_path_request():
    req_data = request.get_json() or {}
    start_id = str(req_data.get('start', ''))
    end_id = str(req_data.get('end', ''))
    traffic = req_data.get('traffic', 'low')
    
    # NEW: Capture vehicle multiplier
    multiplier = float(req_data.get('vehicleMultiplier', 1.0))
    
    nodes = GRAPH_DATA.get('nodes', {})
    edges = GRAPH_DATA.get('edges', [])
    
    if start_id not in nodes or end_id not in nodes:
        return jsonify({"error": "Invalid endpoints sent to routing matrix engine."}), 400

    optimized_path = a_star_search(start_id, end_id, traffic)
    if not optimized_path:
        return jsonify({"error": "No viable spatial interconnecting jumps calculated."}), 404

    # Accumulate metrics
    total_distance = 0.0
    for i in range(len(optimized_path) - 1):
        u, v = str(optimized_path[i]), str(optimized_path[i+1])
        for edge in edges:
            src, tgt = str(edge['source']), str(edge['target'])
            if (src == u and tgt == v) or (src == v and tgt == u):
                total_distance += float(edge.get('distance', 1.0))
                break

    # UPDATED: Applying multiplier logic
    speed_kmh = (30.0 if traffic == "high" else 50.0) / multiplier
    calculated_minutes = int((total_distance / speed_kmh) * 60)
    time_display_string = f"{calculated_minutes}m" if calculated_minutes < 60 else f"{calculated_minutes // 60}h {calculated_minutes % 60}m"
    
    original_distance = round(total_distance * 1.35, 1)
    original_hours = original_distance / (20.0 if traffic == "high" else 40.0)
    fuel_saved = round((original_distance - total_distance) * 0.12 * multiplier, 1)

    return jsonify({
        "path": optimized_path,
        "distance": round(total_distance, 1),
        "time": time_display_string,
        "fuelSaved": max(fuel_saved, 0.5),
        "stops": len(optimized_path),
        "originalDistance": original_distance,
        "originalTime": round(original_hours, 2),
        "originalFuel": round(original_distance * 0.15 * multiplier, 1)
    }), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)