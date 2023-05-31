import folium
import sqlite3
import webbrowser

# Połączenie z bazą danych SQLite
conn = sqlite3.connect('stacje.db')
cursor = conn.cursor()


def display_map():
    """
    Wyświetla mapę ze stacjami w domyślnej przeglądarce internetowej.
    """
    webbrowser.open('map.html')


def create_map():
    """
    Tworzy mapę ze stacjami i zapisuje ją jako plik HTML.
    """
    # Utworzenie mapy folium skoncentrowanej na Polsce
    m = folium.Map(location=[52.237049, 21.017532], zoom_start=6)

    # Zapytanie o stacje i ich współrzędne z bazy danych
    cursor.execute('SELECT stationName, gegrLat, gegrLon FROM stacje')
    stations = cursor.fetchall()

    # Przejście przez stacje i dodanie znaczników na mapie
    for station in stations:
        station_name, lat, lon = station
        folium.Marker(location=[float(lat), float(lon)], popup=station_name).add_to(m)

    # Zapisanie mapy jako plik HTML
    m.save('map.html')

    # Zamknięcie połączenia z bazą danych
    conn.close()


if __name__ == '__main__':
    # Utworzenie mapy ze stacjami
    create_map()

    # Wywołanie funkcji do wyświetlenia mapy
    display_map()
