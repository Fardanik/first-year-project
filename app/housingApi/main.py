import os
import os.path
from functools import wraps

from flask import url_for
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import create_engine, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from app.housingApi.postcode_function import get_manchester_area
import requests

# wrapper so wrapped function just returns a list of ids
def primary_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return [id[0] for id in f(*args, **kwargs)]

    return wrapper


def to_dict(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return [house.to_dict() for house in f(*args, **kwargs)]

    return wrapper


def add_image(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        houses_dicts = f(*args, **kwargs)
        for house_dict in houses_dicts:
            house_dict['image'] = args[0].session.query(Image).filter_by(id=house_dict['id']).first().url
        return houses_dicts
    return wrapper


def flaskify_images(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        id = args[0]
        formatted_images = []
        image_list = f(*args, **kwargs)
        for image in image_list:
            formatted_images.append(url_for('static',
                                            filename=f"images_for_houses/"
                                                     f"{id}/{image}"))
        return formatted_images
    return wrapper


class HouseRequests:
    def __init__(self):
        self.engine = create_engine("sqlite:///app/housingApi/houses_database.db", echo=False)
        Base.metadata.create_all(self.engine)

        self.session_local = sessionmaker(bind=self.engine)
        self.session = self.session_local()

    def add_house(self, bedrooms, bathrooms, postcode, cost_pp_pw, date_added, date_avai_from, link, img_links):
        self.session.query(Image).filter(Image.url == link).delete()
        self.session.query(House).filter(House.url == link).delete()

        house = House(bedrooms=bedrooms, bathrooms=bathrooms, postal_code=postcode, price_pp_pw=cost_pp_pw,
                      bills_inc=True, wifi_inc=True, washing_machine=True, url=link)
        self.session.add(house)
        self.session.commit()
        self.session.refresh(house)

        for url in img_links:
            self.session.add(Image(house_id=house.id, url=url))

        self.session.commit()

    def update_area_for_all_houses(self):
        """
        Updates the area field for all houses in the database.
        """
        # Fetch all houses from the database
        houses = self.session.query(House).all()

        for house in houses:
            if house.postal_code:  # Make sure the house has a postal code
                area = get_manchester_area(house.postal_code)
                if area!= None:
                    house.area = area  # Update the area field
                else:
                    house.area = "Manchester"
                print(f"Updated house ID {house.id} with area: {area}")

        # Commit changes to the database
        self.session.commit()

    @add_image
    @to_dict
    def get_all_houses(self, count):
        return self.session.query(House).limit(count).all()

    @add_image
    @to_dict
    def get_all_in_shortlist(self, ids):

        value = self.session.query(House).filter(House.id.in_(ids)).all()
        return value




    @primary_key
    def get_houses_by_area_code(self, area_code):
        return self.session.query(House).filter(House.postal_code.ilike(f"{area_code}%"))

    @primary_key
    def get_houses_by_price(self, lowest_first=True, area_code=""):
        if area_code == "":
            if lowest_first:
                return self.session.query(House).order_by(House.price_pp_pw.asc())
            else:
                return self.session.query(House).order_by(House.price_pp_pw.desc())
        else:
            if lowest_first:
                return self.session.query(House).filter(House.postal_code.ilike(f"{area_code}%")).order_by(
                    House.price_pp_pw.asc())
            else:
                return self.session.query(House).filter(House.postal_code.ilike(f"{area_code}%")).order_by(
                    House.price_pp_pw.desc())

    def get_all_postcodes(self):
        houses_obj = self.session.query(House).all()

        houses = []
        for house in houses_obj:
            if house.postal_code is not None:
                houses.append(house.postal_code)

        return houses

    def get_house_by_id(self, house_id):
        house = self.session.query(House).filter(House.id == house_id).first()
        if house is not None:
            return house.to_dict()
        return None

    @staticmethod
    @flaskify_images
    def get_images_for_house(house_id):
        return os.listdir(f"app/static/images_for_houses/{house_id}")

    

Base = declarative_base()


class House(Base):
    __tablename__ = 'houses'

    id = Column(Integer, primary_key=True, autoincrement=True)

    bedrooms = Column(Integer)
    bathrooms = Column(Integer)

    postal_code = Column(String)
    x_coord = Column(Integer)
    y_coord = Column(Integer)

    price_pp_pw = Column(Integer)
    deposit_cost = Column(Integer)

    bills_inc = Column(Boolean)
    wifi_inc = Column(Boolean)
    washing_machine = Column(Boolean)
    parking = Column(Integer)

    date_available_from = Column(Integer)
    date_available_until = Column(Integer)
    date_added = Column(Integer)


    epc_rating = Column(Integer)

    url = Column(String)
    area= Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'postal_code': self.postal_code,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'price_pp_pw': self.price_pp_pw,
            'deposit_cost': self.deposit_cost,
            'bills_inc': self.bills_inc,
            'wifi_inc': self.wifi_inc,
            'washing_machine': self.washing_machine,
            'parking': self.parking,
            'date_available_from': self.date_available_from,
            'date_available_until': self.date_available_until,
            'date_added': self.date_added,
            'epc_rating': self.epc_rating,
            'url': self.url,
            'area':self.area

        }




# Run to add houses to database
class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    url = Column(String)


# Transport type
class TransportType(Base):
    __tablename__ = 'transport_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


# Time To Place
class TimeToPlace(Base):
    __tablename__ = 'time_to_place'

    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    transport_type_id = Column(Integer, ForeignKey('transport_types.id'))
    time_to_place = Column(Integer)  # Stored in minutes


if __name__ == "__main__":
    engine = create_engine("sqlite:///houses_database.db", echo=False)
    Base.metadata.create_all(engine)

    session_local = sessionmaker(bind=engine)
    session = session_local()
