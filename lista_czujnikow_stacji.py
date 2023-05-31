import sqlite3






def display_sensory(id_stacja):
    try:
        # nawiązanie połączenia z bazą danych
        conn = sqlite3.connect('stacje.db')

        # utworzenie kursora
        cursor = conn.cursor()

        # wykonanie zapytania SQL
        cursor.execute("SELECT * FROM stanowiska WHERE stationId = ?", (id_stacja,))

        # pobranie wyników zapytania
        results = cursor.fetchall()

        # zamknięcie połączenia z bazą danych
        conn.close()

        return results

    except sqlite3.Error as e:
        print("Wystąpił błąd podczas wykonania zapytania SQL:", str(e))
        return []


if __name__ == '__main__':
    print(display_sensory('117'))
