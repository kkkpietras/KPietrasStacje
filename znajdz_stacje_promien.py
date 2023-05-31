from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import sqlite3

def search_stations(location, radius):
    """
    Wyszukuje stacje w najbliższym, zadanym promieniu (w km) od podanej lokalizacji.

    Parametry:
        - location (str): Opis lokalizacji, np. "Collegium da Vinci, Poznań".
        - radius (float): Promień w kilometrach.

    """

    try:
        # Połączenie z bazą danych SQLite
        conn = sqlite3.connect('stacje.db')
        cursor = conn.cursor()

        # Użycie Geopy do pobrania współrzędnych dla podanej lokalizacji
        geolocator = Nominatim(user_agent='station_search')
        location = geolocator.geocode(location)
        if not location:
            print('Nie znaleziono lokalizacji.')
            return

        # Zapytanie o wszystkie stacje z bazy danych
        cursor.execute('SELECT id, stationName, gegrLat, gegrLon FROM stacje')
        stations = cursor.fetchall()

        # Filtracja stacji znajdujących się w zadanym promieniu
        result = []
        for station in stations:
            station_id, station_name, lat, lon = station
            station_location = (float(lat), float(lon))
            distance = geodesic(location.point, station_location).kilometers
            if distance <= radius:
                result.append((station_id, station_name, distance))

        # Posortowanie wyników według odległości
        result.sort(key=lambda x: x[2])

        # Zwracanie wyników
        return result

    except Exception as e:
        print(f'Wystąpił błąd: {str(e)}')
        return []

