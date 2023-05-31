import tkinter as tk
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from requests.exceptions import RequestException
from bazadanychall import Base, Stacje, Stanowiska, Dane, Indeks
from sqlalchemy import text


def add_sensory(stacja_id, sensory):
    """
    Dodaje sensory do bazy danych dla danej stacji.

    :param stacja_id: ID stacji
    :param sensory: Lista sensory
    """
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    for sensor in sensory:
        existing_sensor = session.query(Stanowiska).filter_by(id=sensor['id']).first()
        if existing_sensor is None:
            s = Stanowiska(
                id=sensor['id'],
                stationId=stacja_id,
                paramName=sensor['param']['paramName'],
                paramFormula=sensor['param']['paramFormula'],
                paramCode=sensor['param']['paramCode'],
                idParam=sensor['param']['idParam']
            )
            session.add(s)
            session.commit()

    session.close()


def wpisz_stacje():
    """
    Pobiera dane o stacjach pomiarowych i zapisuje je w bazie danych.
    """
    text=' '
    try:
        res = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll")
        res.raise_for_status()
        packages_json = res.json()

        packages_dict = []

        if isinstance(packages_json, list):
            packages_dict = packages_json
        elif isinstance(packages_json, dict):
            packages_dict.append(packages_json)

        engine = create_engine('sqlite:///stacje.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.create_all(engine)

        for package in packages_dict:
            id = package.get('id')
            stationName = package.get('stationName')
            gegrLat = package.get('gegrLat')
            gegrLon = package.get('gegrLon')
            city = package.get('city', {})
            city_key = city.get('name')
            commune = city.get('commune', {})
            communeName = commune.get('communeName')
            districtName = commune.get('districtName')
            provinceName = commune.get('provinceName')
            addressStreet = package.get('addressStreet')

            existing_stacja = session.query(Stacje).filter_by(id=id).first()
            if existing_stacja is None:
                p = Stacje(
                    id=id,
                    stationName=stationName,
                    gegrLat=gegrLat,
                    gegrLon=gegrLon,
                    city_key=city_key,
                    communeName=communeName,
                    districtName=districtName,
                    provinceName=provinceName,
                    addressStreet=addressStreet
                )
                session.add(p)
                session.commit()

                res_sensory = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{id}")
                res_sensory.raise_for_status()
                sensory_json = res_sensory.json()

                sensory_dict = []

                if isinstance(sensory_json, list):
                    sensory_dict = sensory_json
                elif isinstance(sensory_json, dict):
                    sensory_dict.append(sensory_json)

                add_sensory(id, sensory_dict)

        print('Liczba stacji pomiarowych:', len(packages_dict))

        session.close()

    except RequestException as e:
        text = 'UWAGA!Wystąpił błąd podczas żądania:', str(e)
        print('Wystąpił błąd podczas żądania:', str(e))
    except json.JSONDecodeError as e:
        print('Błąd dekodowania odpowiedzi JSON:', str(e))
        text = 'UWAGA!Błąd dekodowania odpowiedzi JSON:', str(e)

    return text
