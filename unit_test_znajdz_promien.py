import unittest
from geopy import geocoders
from geopy.distance import geodesic
import sqlite3

from znajdz_stacje_promien import search_stations

class TestSearchStations(unittest.TestCase):
    """
    Klasa testowa dla funkcji search_stations.
    """

    def setUp(self):
        """
        Metoda konfiguracyjna wykonywana przed każdym testem.
        """
        self.geolocator = geocoders.Nominatim(user_agent='station_search')
        self.conn = sqlite3.connect('stacje.db')

    def tearDown(self):
        """
        Metoda czyszcząca wykonywana po każdym teście.
        """
        self.conn.close()

    def test_search_stations(self):
        """
        Testuje funkcję search_stations.
        """
        location = 'Collegium da Vinci, Poznań'
        radius = 5.0

        result = search_stations(location, radius)

        # Sprawdzenie czy zwrócono wyniki
        self.assertIsNotNone(result)

        # Sprawdzenie czy wyniki są posortowane według odległości
        distances = [distance for _, _, distance in result]
        self.assertEqual(distances, sorted(distances))

        # Sprawdzenie czy wszystkie stacje są w zadanym promieniu
        for _, _, distance in result:
            self.assertLessEqual(distance, radius)

        # Sprawdzenie czy znaleziono lokalizację
        location_found = self.geolocator.geocode(location)
        self.assertIsNotNone(location_found)

        # Sprawdzenie czy odległości są obliczane poprawnie
        for station in result:
            station_id, _, _ = station
            cursor = self.conn.cursor()
            cursor.execute('SELECT gegrLat, gegrLon FROM stacje WHERE id = ?', (station_id,))
            station_lat, station_lon = cursor.fetchone()
            station_location = (float(station_lat), float(station_lon))
            distance = geodesic(location_found.point, station_location).kilometers
            self.assertAlmostEqual(distance, station[2], delta=0.01)

if __name__ == '__main__':
    unittest.main()
