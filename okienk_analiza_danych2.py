import tkinter as tk
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from bazadanychall import Dane, Stanowiska
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import spearmanr
import sqlite3


def pobierz_zakres_dat(sensorid):
    """
    Pobiera zakres dat dla danego sensora z bazy danych i wyświetla GUI do wyboru dat.

    Args:
        sensorid (int): ID sensora.

    Returns:
        tuple: Krotka zawierająca datę początkową i datę końcową.
    """
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Sprawdzenie, czy sensorid istnieje w bazie danych
    if not session.query(Stanowiska).filter_by(id=sensorid).first():
        info = f"Brak danych w bazie dla sensora {sensorid}"
    else:
        min_date = session.query(func.min(Dane.date)).filter_by(sensor_id=sensorid).scalar()
        max_date = session.query(func.max(Dane.date)).filter_by(sensor_id=sensorid).scalar()

        if min_date is None or max_date is None:
            info = f"Brak dostępnych danych w bazie dla sensora {sensorid}"
        else:
            info = f"Dostępne dane w bazie dla sensora {sensorid}:\n"
            info += f"Najwcześniejsza data: {min_date.strftime('%Y-%m-%d')}\n"
            info += f"Najpóźniejsza data: {max_date.strftime('%Y-%m-%d')}\n"

    session.close()

    root = tk.Tk()
    root.title("Wyniki")
    root.geometry("300x200")

    label_info = tk.Label(root, text=info)
    label_info.pack()

    def zatwierdz():
        global date_poczatkowa, date_koncowa
        try:
            date_poczatkowa = datetime.strptime(entry_poczatkowa.get(), "%Y-%m-%d")
        except ValueError:
            date_poczatkowa = min_date

        try:
            date_koncowa = datetime.strptime(entry_koncowa.get(), "%Y-%m-%d")
        except ValueError:
            date_koncowa = max_date

        if date_poczatkowa < min_date or date_poczatkowa > max_date:
            date_poczatkowa = min_date

        if date_koncowa < min_date or date_koncowa > max_date:
            date_koncowa = max_date

        analiza_danych(sensorid, date_poczatkowa, date_koncowa)

    label_poczatkowa = tk.Label(root, text="Data początkowa (RRRR-MM-DD):")
    label_poczatkowa.pack()

    default_poczatkowa = min_date.strftime("%Y-%m-%d") if min_date else ""
    entry_poczatkowa = tk.Entry(root)
    entry_poczatkowa.insert(0, default_poczatkowa)
    entry_poczatkowa.pack()

    label_koncowa = tk.Label(root, text="Data końcowa (RRRR-MM-DD):")
    label_koncowa.pack()

    default_koncowa = max_date.strftime("%Y-%m-%d") if max_date else ""
    entry_koncowa = tk.Entry(root)
    entry_koncowa.insert(0, default_koncowa)
    entry_koncowa.pack()

    button_zatwierdz = tk.Button(root, text="Zatwierdź", command=zatwierdz)
    button_zatwierdz.pack()

    root.mainloop()

    return date_poczatkowa, date_koncowa


def analiza_danych(sensorid, data_poczatkowa, data_koncowa):
    """
    Analizuje dane dla danego sensora w zadanym zakresie dat.

    Args:
        sensorid (int): ID sensora.
        data_poczatkowa (datetime.datetime): Data początkowa.
        data_koncowa (datetime.datetime): Data końcowa.
    """
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Wykonaj zapytanie do bazy danych, aby otrzymać wartości dla zadanego zakresu dat i określonego sensora
    result = session.query(Dane).filter(
        Dane.sensor_id == sensorid,
        Dane.date >= data_poczatkowa,
        Dane.date <= data_koncowa
    ).all()

    paramName = session.query(Stanowiska.paramName).filter_by(id=sensorid).scalar()

    if not result:
        info = f"Brak danych w podanym zakresie dla sensora {sensorid}"
    else:
        df = pd.DataFrame([(row.date, row.value) for row in result], columns=['date', 'value'])
        min_value = round(df['value'].min(), 2)
        max_value = round(df['value'].max(), 2)
        min_date = df.loc[df['value'].idxmin(), 'date']
        max_date = df.loc[df['value'].idxmax(), 'date']
        avg_value = round(df['value'].mean(), 2)

        values = df['value'].values
        indices = np.arange(len(values))
        correlation, _ = spearmanr(values, indices)
        correlation = round(correlation, 5)

        info = f"Analiza danych dla czujnika {sensorid}\n"
        info += f"dla parametru: {paramName}\n"
        info += "w zakresie czasu:\n"
        info += f"od {data_poczatkowa}\n"
        info += f"do {data_koncowa}\n"
        info += f"Najmniejsza wartość: {min_value} (Data: {min_date})\n"
        info += f"Największa wartość: {max_value} (Data: {max_date})\n"
        info += f"Średnia wartość: {avg_value}\n"
        info += f"Współczynnik korelacji Spearmana: {correlation}"

    session.close()

    wypisz_wyniki_analizy(info, sensorid)


def wypisz_wyniki_analizy(info, sensorid):
    """
    Wyświetla wyniki analizy w nowym oknie.

    Args:
        info (str): Informacje o wynikach analizy.
        sensorid (int): ID sensora.
    """
    new_window = tk.Toplevel()
    new_window.title("Wyniki analizy")
    new_window.geometry("300x200")

    label_info = tk.Label(new_window, text=info)
    label_info.pack()

    button_wykres = tk.Button(new_window, text="Wykres",
                              command=lambda: wyswietl_wykres(sensorid, date_poczatkowa, date_koncowa))
    button_wykres.pack()


def wyswietl_wykres(sensorid, data_poczatkowa, data_koncowa):
    """
    Wyświetla wykres danych pomiarowych dla danego sensora w zadanym zakresie dat.

    Args:
        sensorid (int): ID sensora.
        data_poczatkowa (datetime.datetime): Data początkowa.
        data_koncowa (datetime.datetime): Data końcowa.
    """
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Wykonaj zapytanie do bazy danych, aby otrzymać wartości dla zadanego zakresu dat i określonego sensora
    result = session.query(Dane).filter(
        Dane.sensor_id == sensorid,
        Dane.date >= data_poczatkowa,
        Dane.date <= data_koncowa
    ).all()

    if not result:
        print("Brak danych w podanym zakresie dla czujnika:", sensorid)
    else:
        paramname = session.query(Stanowiska.paramName).filter_by(id=sensorid).scalar()
        df = pd.DataFrame([(row.date, row.value) for row in result], columns=['date', 'value'])
        df['date'] = pd.to_datetime(df['date'])

        # Generuj wykres punktowy
        plt.scatter(df['date'], df['value'])
        plt.xlabel('Data')
        plt.ylabel('Wartość')
        plt.title('Wykres danych pomiarowych dla czujnika {} dla parametru {}'.format(sensorid, paramname))

        # Dostosuj osie x
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Formatowanie osi x
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatyczny podział osi x

        # Wyświetl wykres
        plt.gcf().autofmt_xdate()  # Dostosowanie etykiet osi x dla lepszej czytelności
        plt.show()

    session.close()


if __name__ == '__main__':
    # Przykładowe użycie:
    # data_poczatkowa = datetime.strptime('2023-01-01', '%Y-%m-%d')
    # data_koncowa = datetime.strptime('2023-12-31', '%Y-%m-%d')

    sensorid = 644
    pobierz_zakres_dat(sensorid)
