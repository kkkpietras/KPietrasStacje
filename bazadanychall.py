from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tworzenie silnika bazy danych SQLite
engine = create_engine('sqlite:///stacje.db', echo=True)

# Tworzenie fabryki sesji
Session = sessionmaker(bind=engine)

# Tworzenie sesji
session = Session()

# Tworzenie bazowego modelu deklaratywnego
Base = declarative_base()


class Stacje(Base):
    """
    Klasa reprezentująca tabelę 'stacje' w bazie danych.

    """
    __tablename__ = 'stacje'
    id1 = Column(Integer, primary_key=True)
    id = Column(String)
    stationName = Column(String)
    gegrLat = Column(String)
    gegrLon = Column(String)
    city_key = Column(String)
    communeName = Column(String)
    districtName = Column(String)
    provinceName = Column(String)
    addressStreet = Column(String)

    def __init__(self, id, stationName, gegrLat, gegrLon, city_key,communeName, districtName, provinceName, addressStreet):
        """
        Inicjalizuje obiekt klasy Stacje.

        :param id: ID stacji
        :param stationName: Nazwa stacji
        :param gegrLat: Szerokość geograficzna
        :param gegrLon: Długość geograficzna
        :param city_key: Klucz miasta
        :param communeName: Nazwa gminy
        :param districtName: Nazwa powiatu
        :param provinceName: Nazwa województwa
        :param addressStreet: Nazwa ulicy
        """
        self.id = id
        self.stationName = stationName
        self.gegrLat = gegrLat
        self.gegrLon = gegrLon
        self.city_key = city_key
        self.communeName = communeName
        self.districtName = districtName
        self.provinceName = provinceName
        self.addressStreet = addressStreet

    def __repr__(self):
        """
        Zwraca reprezentację obiektu klasy Stacje w formacie tekstowym.

        :return: Reprezentacja obiektu klasy Stacje w formacie tekstowym
        """
        return f'{self.id} {self.stationName}'


class Stanowiska(Base):
    """
    Klasa reprezentująca tabelę 'stanowiska' w bazie danych.

    """
    __tablename__ = 'stanowiska'
    id4 = Column(Integer, primary_key=True)
    id = Column(String)
    stationId = Column(String)
    paramName = Column(String)
    paramFormula = Column(String)
    paramCode = Column(String)
    idParam = Column(String)

    def __init__(self, id, stationId, paramName, paramFormula, paramCode, idParam):
        """
        Inicjalizuje obiekt klasy Stanowiska.

        :param id: ID stanowiska
        :param stationId: ID stacji, do której stanowisko należy
        :param paramName: Nazwa parametru
        :param paramFormula: Formuła parametru
        :param paramCode: Kod parametru
        :param idParam: ID parametru
        """
        self.id = id
        self.stationId = stationId
        self.paramName = paramName
        self.paramFormula = paramFormula
        self.paramCode = paramCode
        self.idParam = idParam

class Dane(Base):
        """
        Klasa reprezentująca tabelę 'dane' w bazie danych.

        """
        __tablename__ = 'dane'
        id6 = Column(Integer, primary_key=True)
        sensor_id = Column(String)
        key = Column(String)
        date = Column(DateTime)
        value = Column(Float)

        def __init__(self, sensor_id, key, date, value):
            """
            Inicjalizuje obiekt klasy Dane.

            :param sensor_id: ID czujnika
            :param key: Klucz
            :param date: Data pomiaru
            :param value: Wartość pomiaru
            """
            self.sensor_id = sensor_id
            self.key = key
            self.date = date
            self.value = value

class Indeks(Base):
        """
        Klasa reprezentująca tabelę 'indeks' w bazie danych.

        """
        __tablename__ = 'indeks'
        id8 = Column(Integer, primary_key=True)
        id = Column(String)
        stCalcDate = Column(String)
        stIndexLevel_id = Column(String)
        indexLevelName = Column(String)
        stSourceDataDate = Column(String)

        def __init__(self, id, stCalcDate, stIndexLevel_id, indexLevelName, stSourceDataDate):
            """
            Inicjalizuje obiekt klasy Indeks.

            :param id: ID indeksu
            :param stCalcDate: Data obliczenia
            :param stIndexLevel_id: ID poziomu indeksu
            :param indexLevelName: Nazwa poziomu indeksu
            :param stSourceDataDate: Data źródłowa danych
            """
            self.id = id
            self.stCalcDate = stCalcDate
            self.stIndexLevel_id = stIndexLevel_id
            self.indexLevelName = indexLevelName
            self.stSourceDataDate = stSourceDataDate

if __name__ == '__main__':
    Base.metadata.create_all(engine)

