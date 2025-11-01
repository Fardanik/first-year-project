import json
from functools import wraps

from flask import Blueprint, render_template, request, abort, session, redirect
from app.housingApi.main import HouseRequests
from app.database.main import UserRequests
from app.database.main import DatabaseRequests
from app.housingApi.postcode_function import get_manchester_area

main = Blueprint('main', __name__)


def is_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_id = session.get('session_id')
        if session_id is None:
            return redirect('/login')

        database_requests = DatabaseRequests(session_id=session_id)
        if database_requests.user_id is None:
            return redirect('/login')

        return f(database_requests, *args, **kwargs)

    return wrapper



@main.route('/')
def home():

    house_requests = HouseRequests()
    houses = house_requests.get_all_houses(500)
    return render_template('index.html',houses=houses)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        if len(data['username']) > 0 and len(data['password']) > 0:
            database_requests = DatabaseRequests()
            session_id = database_requests.login(data['username'],
                                              data['password'])
            if session_id != "":
                session['session_id'] = session_id
                return json.dumps({'success': True})

        return json.dumps({'success': False})


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']

        database_requests = DatabaseRequests()
        session_id = database_requests.register(email, password)

        if session_id != "":
            session['session_id'] = session_id
            return json.dumps({'success': True})
        else:
            # user already exists
            return json.dumps({'success': False})



@main.route('/logout')
def logout():
    # TODO: Logout
    return json.dumps({})


@main.route('/messages', methods=['GET', 'POST'])
@is_logged_in
def messages(database_requests):
    if request.method == 'GET':
        chats = database_requests.get_all_chats()

        users = database_requests.get_all_users()

        print(users)

        return render_template('message_page.html', chats=chats,
                               user_id=database_requests.user_id, users=users)
    if request.method == 'POST':
        data = request.get_json()
        match data['type']:
            case 'get_chat_messages':
                chat_id = data['chat_id']

                messages = database_requests.get_chat_messages(chat_id)
                if messages is not None:
                    return json.dumps({'success': True, 'messages': messages})

            case 'send_message':
                chat_id = data['chat_id']
                message = data['message']

                success = database_requests.send_message(chat_id, message)
                return json.dumps({'success': success})

            case 'create_chat':
                chat_name = data['chat_name']
                people = data['people']

                success = database_requests.create_chat(chat_name, people)
                return json.dumps({'success': success})

            case 'leave_chat':
                chat_id = data['chat_id']
                success = database_requests.leave_chat(chat_id)
                return json.dumps({'success': success})

            case 'add_to_group':
                chat_id = data['chat_id']
                user_id = data['user_id']
                # convert name to userid
                user_id = database_requests.name_to_id(user_id)
                success = database_requests.add_to_group(chat_id, user_id)
                return json.dumps({'success': success})

            case 'rename_chat':
                chat_id = data['chat_id']
                name = data['name']
                success = database_requests.rename_chat(chat_id, name)
                return json.dumps({'success': success})

            case _:
                pass
        return json.dumps({'success': False})




@main.route('/my_account', methods=['GET', 'POST'])
@is_logged_in
def my_account(database_requests):
    user_info = database_requests.get_user_info()
    if request.method == 'GET':


        return render_template('my_account_page.html', user_data=user_info, update_user_info=database_requests.update_user_info)
    elif request.method == 'POST':
        data = request.get_json()
        first_name = data.get('firstName')
        gender = data.get('gender')
        age = data.get('age')
        email = data.get('email')
        university = data.get('university')
        bio = data.get('bio')
        pricePerWeek = data.get('pricePerWeek')
        area = data.get('area')
        hobbies = data.get('hobbies')
        print(data)
        database_requests.update_user_info(first_name, email, bio, gender, age, area, hobbies, pricePerWeek, university)

        return render_template('my_account_page.html', user_data=user_info, update_user_info=database_requests.update_user_info)



@main.route('/shortlist')
def shortlist():
    session_id = session.get('session_id')
    if session_id is None:
        return redirect('/login')
    database_requests = DatabaseRequests(session_id=session_id)

    shortlist = database_requests.get_user_shortlist()

    house_requests = HouseRequests()
    houses = house_requests.get_all_in_shortlist(shortlist)
    return render_template('my_shortlist_page.html', shortlist=houses)


@main.route('/property_info/<int:id>', methods=['GET', 'POST'])
def property_info(id):
    if request.method == 'GET':
        house_requests = HouseRequests()
        house = house_requests.get_house_by_id(id)
        if house is None:
            # if the house cannot be found, 404 error
            abort(404)

        images = house_requests.get_images_for_house(id)

        location = house['area']

        is_shortlisted = False

        if session.get('session_id') is not None:
            database_requests = DatabaseRequests(session_id=session['session_id'])
            is_shortlisted = database_requests.is_house_shortlisted(id)

        return render_template('property_information.html', house=house,
                               images=images, location=location,
                               is_shortlisted=is_shortlisted)

    elif request.method == 'POST':
        return add_remove_to_shortlist(id)


@is_logged_in
def add_remove_to_shortlist(database_requests, id):
    data = request.get_json()

    if data['add_shortlist']:
        database_requests.add_house_to_shortlist(id)
        return json.dumps({'success': True})
    else:
        database_requests.remove_house_from_shortlist(id)
        return json.dumps({'success': True})


@main.route('/property_list')
def property_list():
    house_requests = HouseRequests()
    houses = house_requests.get_all_houses(500)
    return render_template('property_list_page.html', houses=houses)


@main.route('/search')
def search():
    return render_template('property_search.html')


# @main.route('/property_search')
# def property_search():
#     return render_template('property_search.html')


@main.route('/user_profile/<int:id>')
def user_profile(id):
    data = UserRequests().get_user_by_id(id)
    userID = id
    username = data['username']
    hobbies = data['hobbies']
    gender = data['gender']
    university = data['university']
    age = data["age"]
    aboutMe = data['aboutMe']
    houseRequirements = data['houseRequirements']

    return render_template('user_profile.html', username=username,
                           hobbies=hobbies, aboutMe=aboutMe,
                           houseRequirements=houseRequirements)
