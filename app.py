from flask import Flask, jsonify, request
from supabase_client import supabase
from utils import calculate_distance, est_ouvert_maintenant
import os

app = Flask(__name__)

@app.route('/api/pharmacies', methods=['GET'])
def trouver_pharmacies():
    produit = request.args.get('produit', '').strip()
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not produit or not lat or not lon:
        return jsonify({"error": "Paramètres manquants: produit, lat, lon"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Coordonnées GPS invalides"}), 400

    # 🔍 Étape 1 : Trouver tous les produits correspondants (disponibles)
    produits = supabase.table('produits').select('*').eq('nom', produit).gt('stock', 0).execute()

    if not produits.data:
        return jsonify([])  # Aucun produit trouvé

    pharmacie_ids = {p['pharmacie_id'] for p in produits.data}
    if not pharmacie_ids:
        return jsonify([])

    # 🔍 Étape 2 : Récupérer les pharmacies concernées
    pharmacies = supabase.table('pharmacies').select('*').in_('id', list(pharmacie_ids)).execute()

    resultat = []
    for ph in pharmacies.data:
        coord = ph.get('coordonnees', {})
        ph_lat = coord.get('latitude')
        ph_lon = coord.get('longitude')

        if ph_lat is None or ph_lon is None:
            continue

        # Calcul distance
        distance = calculate_distance(lat, lon, float(ph_lat), float(ph_lon))

        # Vérifier ouverture
        statut_ouvert = est_ouvert_maintenant(ph.get('horaires'))

        # Trouver le prix du produit demandé
        produit_info = next((p for p in produits.data if p['pharmacie_id'] == ph['id']), None)
        prix = produit_info['prix'] if produit_info else None

        resultat.append({
            "nom": ph['nom'],
            "lieu": ph['lieu'],
            "statut": "ouvert" if statut_ouvert else "fermé",
            "prix": prix,
            "date_publication": produit_info.get('datePublication') if produit_info else None,
            "coordonnees": {"latitude": ph_lat, "longitude": ph_lon},
            "telephone": ph.get('telephone'),
            "distance_km": round(distance, 2)
        })

    # 🧠 Agent IA : tri par distance puis par prix
    resultat.sort(key=lambda x: (x['distance_km'], x.get('prix', float('inf'))))

    return jsonify(resultat)

# 🔥 Route de santé (pour Render)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "agent": "LAFYA IA Actif"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
