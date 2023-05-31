import sqlite3

def display_stations2(city):
    """
    Wyświetla informacje o stacjach z bazy danych dla podanego miasta.

    :param city: Nazwa miasta
    :return: Wyniki zapytania SQL
    """
    try:
        # nawiązanie połączenia z bazą danych
        conn = sqlite3.connect('stacje.db')

        # utworzenie kursora
        cursor = conn.cursor()

        # wykonanie zapytania SQL
        cursor.execute("SELECT * FROM stacje WHERE city_key = ?", (city,))

        # pobranie wyników zapytania
        results = cursor.fetchall()

        # zamknięcie połączenia z bazą danych
        conn.close()

        return results

    except sqlite3.Error as e:
        print("Wystąpił błąd podczas wykonania zapytania SQL:", str(e))
        return []


if __name__ == '__main__':
    print(display_stations2('Kalisz'))
