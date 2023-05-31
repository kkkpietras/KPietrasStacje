import sqlite3

def display_stations():
    """
    Wyświetla informacje o stacjach z bazy danych.

    :return: Tekstowa reprezentacja stacji w formacie tabeli.
    """
    try:
        # nawiązanie połączenia z bazą danych
        conn = sqlite3.connect('stacje.db')

        # utworzenie kursora
        cursor = conn.cursor()

        # wykonanie zapytania SQL
        cursor.execute("SELECT * FROM stacje")

        # pobranie wyników zapytania
        results = cursor.fetchall()

        # określenie szerokości kolumn
        column_widths = [20, 20, 30]

        # utworzenie stringa wynikowego
        result_string = f'{"MIASTO":<{column_widths[0]}} {"ID STACJI":<{column_widths[1]}} {"ADRES":<{column_widths[2]}}\n'
        for row in results:
            miasto = row[5] if row[5] is not None else ""
            id_stacji = str(row[1]) if row[1] is not None else ""
            adres = row[9] if row[9] is not None else ""
            result_string += f'{miasto:<{column_widths[0]}} {id_stacji:<{column_widths[1]}} {adres:<{column_widths[2]}}\n'

        # zakończenie połączenia z bazą danych
        conn.close()

        return result_string

    except sqlite3.Error as e:
        return "Wystąpił błąd podczas wykonania zapytania SQL: " + str(e)
