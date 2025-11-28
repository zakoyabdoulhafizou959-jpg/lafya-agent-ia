import math
import pytz
from datetime import datetime

def calculate_distance(lat1, lon1, lat2, lon2):
    """Retourne la distance en km entre deux points GPS."""
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def est_ouvert_maintenant(horaires_json):
    """
    Vérifie si la pharmacie est ouverte maintenant.
    Format attendu: {"lundi": "08:00-18:00", "mardi": "08:00-18:00", ..., "dimanche": "fermé"}
    """
    if not horaires_json:
        return False

    tz = pytz.timezone('Africa/Niamey')  # Fuseau horaire du Niger
    now = datetime.now(tz)
    jour_semaine = now.strftime('%A').lower()
    heure_actuelle = now.time()

    # Mapper le jour en français (optionnel) ou utiliser anglais
    jour_map = {
        'monday': 'lundi',
        'tuesday': 'mardi',
        'wednesday': 'mercredi',
        'thursday': 'jeudi',
        'friday': 'vendredi',
        'saturday': 'samedi',
        'sunday': 'dimanche'
    }
    jour_fr = jour_map.get(jour_semaine, jour_semaine)

    plage = horaires_json.get(jour_fr, '').strip()
    if not plage or plage == 'fermé':
        return False

    try:
        debut_str, fin_str = plage.split('-')
        debut = datetime.strptime(debut_str.strip(), '%H:%M').time()
        fin = datetime.strptime(fin_str.strip(), '%H:%M').time()
        return debut <= heure_actuelle <= fin
    except:
        return False
