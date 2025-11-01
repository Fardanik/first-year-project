# SQLAlchemy Python file for creating the database with all foreign key
# relations
from functools import wraps

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Text, Boolean, Float
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, \
    joinedload
from sqlalchemy import create_engine, inspect
import hashlib
from bcrypt import gensalt

import time
from datetime import datetime

# Define the base for our classes

engine = create_engine('sqlite:///app/database/database.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Define the Users table
class User(Base):
    __tablename__ = 'Users'
    userID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    email = Column(String)
    emailNotifications = Column(Boolean, nullable=False)
    aboutUser = Column(String)
    gender = Column(String)
    age = Column(Integer)

class UserPropertyShortlistLink(Base):
    __tablename__ = 'UserPropertyShortlistLink'
    UserPropertyShortlistLinkID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('Users.userID'))
    houseID = Column(Integer)

class Sessions(Base):
    __tablename__ = 'Sessions'
    pk = Column(Integer, primary_key=True)
    sessionID = Column(String, nullable=False)
    userID = Column(Integer, ForeignKey('Users.userID'))
    expires = Column(Integer)


# Define the Chats table
class Chat(Base):
    __tablename__ = 'Chats'
    chatID = Column(Integer, primary_key=True)
    chatName = Column(String, nullable=False)



# Define the UsersChatsLink table (for many-to-many relationship)
class UsersChatsLink(Base):
    __tablename__ = 'UsersChatsLink'
    usersChatsLinkID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    chatID = Column(Integer, ForeignKey('Chats.chatID'), nullable=False)
    #user = relationship('User', back_populates='chats')
    #chat = relationship('Chat', back_populates='users')


# Define the ChatMessages table
class ChatMessage(Base):
    __tablename__ = 'ChatMessages'
    messageID = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    chatID = Column(Integer, ForeignKey('Chats.chatID'), nullable=False)
    sender = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    dateSent = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'messageID': self.messageID,
            'message': self.message,
            'chatID': self.chatID,
            'sender': self.sender,
            'dateSent': datetime.fromtimestamp(self.dateSent).strftime('%Y-%m-%d %H:%M:%S'),
        }

    #chat = relationship('Chat', back_populates='messages')
#sender_user = relationship('User')
    #properties = relationship('MessagePropertyLink', back_populates='message')
    #reactions = relationship('MessageReaction', back_populates='message')


# Define the MessagePropertyLink table
class MessagePropertyLink(Base):
    __tablename__ = 'MessagePropertyLink'
    messagePropertyLinkID = Column(Integer, primary_key=True)
    messageID = Column(Integer, ForeignKey('ChatMessages.messageID'),
                       nullable=False)
    propertyID = Column(Integer, ForeignKey('Properties.propertyID'),
                        nullable=False)
    #message = relationship('ChatMessage', back_populates='properties')
    #property = relationship('Properties', back_populates='message_property')


# Define the MessageReactions table
class MessageReaction(Base):
    __tablename__ = 'MessageReactions'
    messageReactionID = Column(Integer, primary_key=True)
    messageID = Column(Integer, ForeignKey('ChatMessages.messageID'),
                       nullable=False)
    sender = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    reaction = Column(String, nullable=False)
    #message = relationship('ChatMessage', back_populates='reactions')


# Define the Properties table
class Property(Base):
    __tablename__ = 'Properties'
    propertyID = Column(Integer, primary_key=True)
    propertyName = Column(String, nullable=False)
    propertyAPIReference = Column(String, nullable=False)
    #chats = relationship('PropertyChatLink', back_populates='property')


# Define the PropertyChatLink table
class PropertyChatLink(Base):
    __tablename__ = 'PropertyChatLink'
    propertyChatLinkID = Column(Integer, primary_key=True)
    propertyID = Column(Integer, ForeignKey('Properties.propertyID'),
                        nullable=False)
    chatID = Column(Integer, ForeignKey('Chats.chatID'), nullable=False)
    #property = relationship('Property', back_populates='chats')
    #chat = relationship('Chat', back_populates='properties')


# Define the Hobbies table
class Hobby(Base):
    __tablename__ = 'Hobbies'
    hobbyID = Column(Integer, primary_key=True)
    hobbyName = Column(String, nullable=False)


# Define the UsersHobbiesLink table
class UsersHobbiesLink(Base):
    __tablename__ = 'UsersHobbiesLink'
    usersHobbiesLinkID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    hobbyID = Column(Integer, ForeignKey('Hobbies.hobbyID'), nullable=False)
    #user = relationship('User', back_populates='hobbies')
    #hobby = relationship('Hobby')


# Define the Universities table
class University(Base):
    __tablename__ = 'Universities'
    universityID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)


# Define the UsersUniversitiesLink table
class UsersUniversitiesLink(Base):
    __tablename__ = 'UsersUniversitiesLink'
    usersUniversityLinkID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    universityID = Column(Integer, ForeignKey('Universities.universityID'),
                          nullable=False)
    #user = relationship('User', back_populates='universities')
    #university = relationship('University')


# Define the Areas table
class Area(Base):
    __tablename__ = 'Areas'
    areaID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    postcode = Column(String, nullable=False)


# Define the UserHouseRequirements table
class UserHouseRequirements(Base):
    __tablename__ = 'UserHouseRequirements'
    userHouseRequirementsID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('Users.userID'), nullable=False)
    maxDistToStation = Column(Integer, nullable=False)
    maxDistToBusStop = Column(Integer, nullable=False)
    maxDistToCityCenter = Column(Integer, nullable=False)
    maxDistToUni = Column(Integer, nullable=False)
    houseRooms = Column(Integer, nullable=False)
    maxPrice = Column(Integer, nullable=False)
    knowRoommates = Column(Boolean, nullable=False)



# Define the UserHouseRequirementsAreasLink table
class UserHouseRequirementsAreasLink(Base):
    __tablename__ = 'UserHouseRequirementsAreasLink'
    UserHouseRequirementsAreasID = Column(Integer, primary_key=True)
    userHouseRequirementsID = Column(Integer, ForeignKey(
        'UserHouseRequirements.userHouseRequirementsID'), nullable=False)
    areaID = Column(Integer, ForeignKey('Areas.areaID'), nullable=False)



def msg_to_dict(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        messages = f(*args, **kwargs)
        formatted_messages = []
        if messages is None:
            return None
        for message in messages:
            formatted_messages.append(message.to_dict())
        return formatted_messages
    return wrapper



def msg_to_dict(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        messages = f(*args, **kwargs)
        formatted_messages = []
        if messages is None:
            return None
        for message in messages:
            formatted_messages.append(message.to_dict())
        return formatted_messages
    return wrapper



class DatabaseRequests:
    def __init__(self, session_id=None):
        create_database()
        self.user_id = None
        self.session = Session()
        self.register('test', 'test')
        self.register('test2', 'test')

        if session_id is not None:
            try:
                self.user_id = self.session.query(Sessions).filter(
                    Sessions.sessionID == session_id).first().userID
            except NoResultFound:
                self.user_id = None

    def rename_chat(self, chat_id, name):
        self.session.query(Chat).filter(Chat.chatID == chat_id).update({
            Chat.chatName: name})
        self.session.commit()

    def update_user_info(self, username, email, aboutUser, gender, age, area, hobbies, pricePerWeek, university_name):
        user_to_update = self.session.query(User).filter_by(userID=self.user_id).first()
        user_to_update.username = username
        user_to_update.email = email
        user_to_update.aboutUser = aboutUser
        user_to_update.gender = gender
        user_to_update.age = age
        self.session.commit()

        userHouseRequirementsL = self.session.query(UserHouseRequirements).filter(UserHouseRequirements.userID == self.user_id).first()
        if not userHouseRequirementsL:
            userHouseRequirementsL = UserHouseRequirements(userID = self.user_id, maxDistToStation=0, maxDistToBusStop=0, maxDistToCityCenter=0, maxDistToUni=0, houseRooms=0, maxPrice=0, knowRoommates=0 )
            self.session.add(userHouseRequirementsL)



        userHouseRequirementsL.maxPrice = pricePerWeek








        self.session.commit()



        area_id = self.session.query(Area).filter(Area.name==area).first()
        if not area_id:
            area_id = Area(name=area, postcode="")
            self.session.add(area_id)
        self.session.commit()

        link = self.session.query(UserHouseRequirementsAreasLink).filter(UserHouseRequirementsAreasLink.userHouseRequirementsID == userHouseRequirementsL.userHouseRequirementsID).first()
        if not link:
            link = UserHouseRequirementsAreasLink(userHouseRequirementsID=userHouseRequirementsL.userHouseRequirementsID, areaID=area_id.areaID)
            self.session.add(link)

        link.areaID = area_id.areaID
        self.session.commit()
        print(f"{link.areaID} HWBDHW")
        self.session.add(link)

        university = self.session.query(University).filter_by(name=university_name).first()

        if not university:
            # If the university doesn't exist, create a new record
            university = University(name=university_name, lat=0, long=0)
            self.session.add(university)
            self.session.commit()

        university_link = self.session.query(UsersUniversitiesLink).filter(UsersUniversitiesLink.userID == self.user_id).first()
        if not university_link:
            university_link = UsersUniversitiesLink(userID=self.user_id, universityID=university.universityID)
            self.session.add(university_link)
        university_link.universityID = university.universityID

        self.session.commit()




    def is_logged_in(self):
        return self.user_id is not None

    def get_user_shortlist(self):
        query = self.session.query(UserPropertyShortlistLink.houseID).filter(
            UserPropertyShortlistLink.userID == self.user_id)
        print(query)
        shortlisted_house_ids = (self.session.query(UserPropertyShortlistLink.houseID).filter(UserPropertyShortlistLink.userID==self.user_id).all())
        print(self.user_id)
        shortlisted_house_ids = [shortlisted_house_id[0] for shortlisted_house_id in shortlisted_house_ids]
        return shortlisted_house_ids

    def add_house_to_shortlist(self, houseID):
        new_record = UserPropertyShortlistLink(userID=self.user_id, houseID=houseID)
        self.session.add(new_record)
        self.session.commit()

    def is_house_shortlisted(self, houseID):
        if self.user_id is None:
            return False
        return self.session.query(UserPropertyShortlistLink).filter(
            UserPropertyShortlistLink.userID==self.user_id,
            UserPropertyShortlistLink.houseID==houseID).count() > 0

    def remove_house_from_shortlist(self, houseID):
        if self.user_id is None:
            return
        self.session.query(UserPropertyShortlistLink).filter(
            UserPropertyShortlistLink.houseID == houseID,
            UserPropertyShortlistLink.userID == self.user_id
        ).delete()
        self.session.commit()

    def add_to_group(self, chat_id, user_id):
        if self.user_id is None:
            return False

        self.session.add(UsersChatsLink(chatID=chat_id,
                                        userID=user_id))

        self.session.commit()

        return True

    def name_to_id(self, user_name):
        return self.session.query(User).filter(User.email == user_name).first().userID

    def get_user_info(self):
            user = self.session.query(User).filter(
                User.userID == self.user_id).first()

            if user:
                hobbies = (
                    self.session.query(Hobby.hobbyName)
                    .join(UsersHobbiesLink,
                          UsersHobbiesLink.hobbyID == Hobby.hobbyID)
                    .filter(UsersHobbiesLink.userID == self.user_id)
                    .all()
                )

                try:
                    hobby_list = [hobby[0] for hobby in hobbies]
                except:
                    hobby_list = []


                house_requirements = (
                    self.session.query(UserHouseRequirements)
                    .filter(UserHouseRequirements.userID == self.user_id)
                    .first()
                )

                house_requirements_dict = None
                if house_requirements:

                    area = (
                        self.session.query(Area.name)
                        .filter(UserHouseRequirements.userID == self.user_id)
                        .filter(UserHouseRequirementsAreasLink.userHouseRequirementsID == UserHouseRequirements.userHouseRequirementsID)
                        .filter(UserHouseRequirementsAreasLink.areaID == Area.areaID)
                        .first()
                    )
                    if area:
                        area = area[0]
                    else:
                        area = " "


                    house_requirements_dict = {
                        "maxDistToStation": house_requirements.maxDistToStation,
                        "maxDistToBusStop": house_requirements.maxDistToBusStop,
                        "maxDistToCityCenter": house_requirements.maxDistToCityCenter,
                        "maxDistToUni": house_requirements.maxDistToUni,
                        "houseRooms": house_requirements.houseRooms,
                        "maxPrice": house_requirements.maxPrice,
                        "knowRoommates": house_requirements.knowRoommates,
                        "areas": area,
                    }


                university = (
                    self.session.query(University.name).filter(self.user_id == UsersUniversitiesLink.userID).filter(
                        UsersUniversitiesLink.universityID == University.universityID).first())
                if university is None:
                    university = " "
                return( {
                    "userID": user.userID,
                    "username": user.username,
                    "password": user.password,
                    "salt": user.salt,
                    "email": user.email,
                    "emailNotifications": user.emailNotifications,
                    "gender": user.gender,
                    "university": university[0],
                    "age": user.age,
                    "aboutMe": user.aboutUser,
                    "hobbies": hobby_list,
                    "houseRequirements": house_requirements_dict
                })
            return None


    def login(self, inp_username, inp_password):
        user = self.session.query(User).filter_by(
            username=inp_username).first()

        if user is not None:
            inp_password_hash = self.__hash_password(inp_password, user.salt)
            if inp_password_hash == user.password:
                self.user_id = user.userID
                return self.create_user_session()

        return ""

    def register(self, username, password):
        if (self.session.query(User).filter_by(username=username).first() is
                not None):
            return ""

        salt = gensalt().decode('utf8')
        password_hash = self.__hash_password(password, salt)

        self.session.add(User(username=username, password=password_hash,
                              salt=salt, emailNotifications=False,
                              email=username, aboutUser="", gender="", age=0))


        self.session.commit()

        return self.create_user_session()

    def get_all_chats(self):
        if self.user_id is not None:

            return (self.session.query(
                Chat
            ).filter(
                User.userID == UsersChatsLink.userID
            ).filter(
                UsersChatsLink.chatID == Chat.chatID
            ).filter(
                UsersChatsLink.userID == self.user_id
            ).all())
        else:
            return None

    @msg_to_dict
    def get_chat_messages(self, chat_id, max=500):

        if self.user_id is not None:
            if self.session.query(UsersChatsLink).filter(UsersChatsLink.chatID == chat_id, UsersChatsLink.userID == self.user_id).count() > 0:
                messages = self.session.query(ChatMessage).filter(
                    ChatMessage.chatID == chat_id).all()
                return messages
        return None

    def create_user_session(self):
        session_id = gensalt().decode('utf8')
        expire_date = time.time()

        self.session.add(Sessions(sessionID=session_id, userID=self.user_id,
                                 expires=expire_date))

        self.session.commit()

        return session_id

    def send_message(self, chat_id, message):
        if self.user_id is not None:
            if self.session.query(UsersChatsLink).filter(
                    UsersChatsLink.chatID == chat_id, UsersChatsLink.userID
                                                      == self.user_id).count() > 0:
                self.session.add(ChatMessage(message=message,
                                             chatID=chat_id,
                                             sender=self.user_id,
                                             dateSent=time.time()))
                self.session.commit()
                return True
        return False

    def create_chat(self, chat_name, people):
        if self.user_id is not None:
            new_chat = Chat(chatName=chat_name)
            self.session.add(new_chat)
            self.session.commit()

            # remove duplicates and ensure creator is in group
            people = [person for person in people if person != self.user_id]
            people = list(dict.fromkeys(people))
            people.append(self.user_id)

            for person in people:
                self.session.add(UsersChatsLink(chatID=new_chat.chatID,
                                                userID=person))
            self.session.commit()
            return True
        return False

    def leave_chat(self, chat_id):
        if self.user_id is not None:
            self.session.query(UsersChatsLink).filter(
                UsersChatsLink.chatID == chat_id,
                UsersChatsLink.userID == self.user_id).delete()
            self.session.commit()
            return True
        return False

    def get_all_users(self):
        users = self.session.query(User).all()

        formatted_users = []

        for user in users:
            if user.email != None:
                formatted_users.append(user.email)

        return formatted_users

    @staticmethod
    def __hash_password(password, salt):
        return hashlib.sha512(f"{password}{salt}".encode()).hexdigest()


class UserRequests:
    def __init__(self, db_url='sqlite:///app/database/database.db'):

        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_user_by_id(self, user_id):

        user = self.session.query(User).filter(
            User.userID == user_id).first()

        if user:

            hobbies = (
                self.session.query(Hobby.hobbyName)
                .join(UsersHobbiesLink,
                      UsersHobbiesLink.hobbyID == Hobby.hobbyID)
                .filter(UsersHobbiesLink.userID == user_id)
                .all()
            )

            hobby_list = [hobby[0] for hobby in hobbies]


            house_requirements = (
                self.session.query(UserHouseRequirements)
                .filter(UserHouseRequirements.userID == user_id)
                .first()
            )

            house_requirements_dict = None
            if house_requirements:
                # Query areas associated with house requirements
                areas = (
                    self.session.query(Area.name)
                    .join(UserHouseRequirements.areas)
                    .filter(UserHouseRequirements.userID == user_id)
                    .all()
                )
                area_list = [area[0] for area in areas]

                house_requirements_dict = {
                    "maxDistToStation": house_requirements.maxDistToStation,
                    "maxDistToBusStop": house_requirements.maxDistToBusStop,
                    "maxDistToCityCenter": house_requirements.maxDistToCityCenter,
                    "maxDistToUni": house_requirements.maxDistToUni,
                    "houseRooms": house_requirements.houseRooms,
                    "maxPrice": house_requirements.maxPrice,
                    "knowRoommates": house_requirements.knowRoommates,
                    "areas": area_list,
                }


            return {
                "userID": user.userID,
                "username": user.username,
                "password": user.password,
                "salt": user.salt,
                "email": user.email,
                "emailNotifications": user.emailNotifications,
                "gender": user.gender,
                "university": user.university,
                "age": user.age,
                "aboutMe": user.aboutMe,
                "hobbies": hobby_list,
                "houseRequirements": house_requirements_dict
            }
        return None


def create_database():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
    session = Session()

    # Check if tables exist
    inspector = inspect(engine)
    print("Tables in database:", inspector.get_table_names())

    # Check if data exists in the Chats table
    chats = session.query(Chat).all()
    print(f"Number of chats: {len(chats)}")
    for chat in chats:
        print(f"Chat ID: {chat.chatID}, Chat Name: {chat.chatName}")

    # Check if data exists in the Users table
    users = session.query(User).all()
    print(f"Number of users: {len(users)}")
    for user in users:
        print(f"User ID: {user.userID}, Username: {user.username}")

    # Check if data exists in the ChatMessages table
    messages = session.query(ChatMessage).all()
    print(f"Number of messages: {len(messages)}")
    for message in messages:
        print(
            f"Message ID: {message.messageID}, Sender: {message.sender}, Message: {message.message}")
