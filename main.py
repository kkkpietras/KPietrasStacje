import tkinter as tk
from sqlalchemy import create_engine
import sqlite3
import lista_czujnikow_stacji
from bazadanychall import Base
import import_stacje
from lista_stacji_all import display_stations
import lista_stacji_miejscowosc
import znajdz_stacje_promien
import wpis_danych_pomiarow
import okienk_analiza_danych2
import mapa_stacji

def create_database():
    """
    Tworzy bazę danych SQLite i tabelę.
    """
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Base.metadata.create_all(engine)
    text_area.delete("1.0", "end")
    text_area.insert("end", "baza danych została utworzona.")
    print("Pusta baza danych została utworzona.")

def on_button_click():
    """
    Wywoływane po kliknięciu przycisku "Utwórz bazę danych".
    """
    create_database()

def on_button2_click():
    """
    Wywoływane po kliknięciu przycisku "Importuj STACJE do bazy danych".
    """
    import_stacje.wpisz_stacje()
    text_area.delete("1.0", "end")
    text_area.insert("end", import_stacje.wpisz_stacje())

def display_string():
    """
    Wyświetla listę wszystkich stacji.
    """
    string = display_stations()
    new_window = tk.Toplevel(root)
    text_area = tk.Text(new_window, height=10, width=50)
    text_area.insert(tk.END, string)
    text_area.pack(fill=tk.BOTH, expand=True)

def display_string2(city):
    """
    Wyświetla stacje dla podanego miasta.
    """
    results = lista_stacji_miejscowosc.display_stations2(city)

    if not results:
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "Nie znaleziono informacji o stacjach w podanym mieście.")
        return

    column_widths = [15, 10, 30]
    string = f'{"MIASTO":<{column_widths[0]}} {"ID STACJI":<{column_widths[1]}} {"ADRES":<{column_widths[2]}}\n'
    for row in results:
        miasto = row[5] if row[5] is not None else ""
        id_stacji = str(row[1]) if row[1] is not None else ""
        adres = row[9] if row[9] is not None else ""
        string += f'{miasto:<{column_widths[0]}} {id_stacji:<{column_widths[1]}} {adres:<{column_widths[2]}}\n'

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, string)

def display_string3(idstacja):
    """
    Wyświetla stanowiska pomiarowe dla podanej stacji.
    """
    results = lista_czujnikow_stacji.display_sensory(idstacja)

    if results:
        text_area.delete("1.0", "end")
        text_area.insert("end", f"Dostępne stanowiska pomiarowe dla stacji o id {idstacja}:\n")
        text_area.insert("end", "{:<10s} {:<20s}\n".format("ID stanowiska", "Nazwa parametru"))
        text_area.insert("end", "-" * 30 + "\n")
        for result in results:
            text_area.insert("end", "{:<10s} {:<20s}\n".format(str(result[1]), result[3]))
    else:
        text_area.delete("1.0", "end")
        text_area.insert("end", "Nie znaleziono informacji o stanowiskach pomiarowych dla podanej stacji.")

def wpisz_dane_do_bazy(sensorid):
    """
    Wpisuje dane pomiarowe do bazy danych dla podanego czujnika.
    """
    def is_valid_sensor(sensor_id):
        conn = sqlite3.connect('stacje.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Stanowiska WHERE id = ?", (sensor_id,))
        result = cursor.fetchone()[0]
        conn.close()
        return result > 0

    if is_valid_sensor(sensorid):
        wpis_danych_pomiarow.wpisz_dane(sensorid)
        text_area.delete("1.0", "end")
        text_area.insert("end", wpis_danych_pomiarow.wpisz_dane(sensorid))
    else:
        text_area.delete("1.0", "end")
        text_area.insert("end", "Nie znaleziono informacji o danych pomiarowych dla podanego czujnika.")

def open_new_window():
    """
    Otwiera nowe okno dla wyszukiwania stacji w podanym mieście.
    """
    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie stacji w mieście")
    label = tk.Label(new_window, text="Podaj nazwę miasta:")
    label.pack()
    entry = tk.Entry(new_window)
    entry.pack()
    button5 = tk.Button(new_window, text="Wyświetl stacje", command=lambda: display_string2(entry.get()))
    button5.pack()

def open_new_window2():
    """
    Otwiera nowe okno dla wyszukiwania stacji w podanym promieniu.
    """
    def search_button_click():
        location = location_entry.get()
        radius_entry_value = radius_entry.get()

        try:
            radius = float(radius_entry_value)
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, 'Podany promień nie jest liczbą.')
            return

        result = znajdz_stacje_promien.search_stations(location, radius)

        if result:
            result_text.delete(1.0, tk.END)
            string = f'Stacje w promieniu {radius} km od {location}:\n'
            result_text.insert(tk.END, string)
            column_widths = [10, 40, 15]
            string = f'{"ID STACJI":<{column_widths[0]}} {"NAZWA STACJI":<{column_widths[1]}} {"ODLEGŁOŚĆ":<{column_widths[2]}}\n'
            for station in result:
                station_id, station_name, distance = station
                string += f'{station_id:<{column_widths[0]}} {station_name:<{column_widths[1]}} {distance:.2f} km\n'
            result_text.insert(tk.END, string)
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f'Stacje w promieniu {radius} km od {location}:\nNie znaleziono stacji w zadanym promieniu.')

    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie stacji")
    location_label = tk.Label(new_window, text='Lokalizacja:')
    location_label.pack()
    location_entry = tk.Entry(new_window)
    location_entry.pack()
    radius_label = tk.Label(new_window, text='Promień (km):')
    radius_label.pack()
    radius_entry = tk.Entry(new_window)
    radius_entry.pack()
    search_button = tk.Button(new_window, text='Wyszukaj', command=search_button_click)
    search_button.pack()
    result_text = tk.Text(new_window)
    result_text.pack()

def open_new_window3():
    """
    Otwiera nowe okno dla wyszukiwania czujników stacji.
    """
    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie czujników stacji")
    label = tk.Label(new_window, text="Podaj ID stacji:")
    label.pack()
    entry = tk.Entry(new_window)
    entry.pack()
    button5 = tk.Button(new_window, text="Wyświetl czujniki", command=lambda: display_string3(entry.get()))
    button5.pack()

def open_new_window4():
    """
    Otwiera nowe okno dla wpisywania danych pomiarowych.
    """
    new_window = tk.Toplevel(root)
    new_window.title("Dane pomiarowe")
    label = tk.Label(new_window, text="Podaj ID czujnika:")
    label.pack()
    entry = tk.Entry(new_window)
    entry.pack()
    button9 = tk.Button(new_window, text="Wpisz dane do bazy danych", command=lambda: wpisz_dane_do_bazy(entry.get()))
    button9.pack()
    button10 = tk.Button(new_window, text="Analiza danych pomiarowych", command=lambda: okienk_analiza_danych2.pobierz_zakres_dat(entry.get()))
    button10.pack()

def mapa():
    """
    Tworzy i wyświetla mapę stacji.
    """
    mapa_stacji.create_map()
    mapa_stacji.display_map()

root = tk.Tk()
button = tk.Button(root, text="Utwórz bazę danych", command=on_button_click)
button.grid(row=0, column=0, padx=10, pady=10)
button2 = tk.Button(root, text="Importuj STACJE do bazy danych", command=on_button2_click)
button2.grid(row=1, column=0, padx=10, pady=10)
button3 = tk.Button(root, text="Lista stacji w Polsce!", command=display_string)
button3.grid(row=2, column=0, padx=10, pady=10)
button4 = tk.Button(root, text="Wyszukaj w miejscowości", command=open_new_window)
button4.grid(row=3, column=0, padx=10, pady=10)
button6 = tk.Button(root, text="Wyszukaj w promieniu", command=open_new_window2)
button6.grid(row=4, column=0, padx=10, pady=10)
button7 = tk.Button(root, text="Wypisz czujniki", command=open_new_window3)
button7.grid(row=5, column=0, padx=10, pady=10)
button8 = tk.Button(root, text="Dane pomiarowe", command=open_new_window4)
button8.grid(row=6, column=0, padx=10, pady=10)
button12 = tk.Button(root, text="Mapa stacji", command=mapa)
button12.grid(row=7, column=0, padx=10, pady=10)
text_area = tk.Text(root, height=10, width=50)
text_area.grid(row=0, column=1, rowspan=8, padx=10, pady=10)
root.mainloop()
