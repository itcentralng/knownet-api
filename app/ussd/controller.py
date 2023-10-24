from flask import Blueprint, request
from app.user.model import User

from app.ussd.model import *
from app.ussd.schema import *
from helpers.sms import send_sms

bp = Blueprint('ussd', __name__)

@bp.post('/ussd')
def listed_to_ussd():
    serviceCode = request.form.get('serviceCode')
    phone = request.form.get('phoneNumber')
    session_id = request.form.get('sessionId')
    networkCode = request.form.get('networkCode')
    selection = request.form.get('text')
    user = User.get_by_phone(phone)
    if not user:
        user = User.create('', 'english', phone, phone, 'user')
    session = Ussd.get_by_session_id(session_id)
    if session:
        if selection.split('*')[-1] == '0':
            return globals()[session.previous](selection=selection, session_id=session_id, user=user)
        return globals()[session.stage](selection=selection, session_id=session_id, user=user)
    return start(selection=selection, session_id=session_id, user=user)

@bp.post('/events')
def handle_events():
    return "Event Received"

def start(**kwargs):
    text = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    if user.is_set:
        Ussd.create_or_update(kwargs['session_id'], 'select_service', previous='start')
        response = f"CON Welcome back {user.name} what do you want to do today?.\n"
        response += "1. Update your name\n"
        response += "2. Update your language\n"
        response += "3. Change your password\n"
    else:
        Ussd.create_or_update(kwargs['session_id'], 'select_service', previous='start')
        response = f"CON Welcome to KnowNet.\n"
        response += "1. Set your name\n"
        response += "2. Set your language\n"
        response += "3. Set your password\n"
    return response

def select_service(**kwargs):
    text = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    if user.is_set:
        if text == '1':
            Ussd.create_or_update(kwargs['session_id'], 'update_user_name', previous='start')
            return update_user_name(**kwargs)
        elif text == '2':
            Ussd.create_or_update(kwargs['session_id'], 'update_user_language', previous='start')
            return update_user_language(**kwargs)
        elif text == '3':
            Ussd.create_or_update(kwargs['session_id'], 'update_user_password', previous='start')
            return update_user_password(**kwargs)
    else:
        if text == '1':
            Ussd.create_or_update(kwargs['session_id'], 'update_user_name', previous='start')
            return update_user_name(**kwargs)
        elif text == '2':
            Ussd.create_or_update(kwargs['session_id'], 'update_user_language', previous='start')
            return update_user_language(**kwargs)
        elif text == '3':
            Ussd.create_or_update(kwargs['session_id'], 'set_user_password', previous='start')
            return set_user_password(**kwargs)

def update_user_name(**kwargs):
    response = "CON Enter your name:\n"
    Ussd.create_or_update(kwargs['session_id'], 'do_update_user_name', 'start')
    return response

def update_user_language(**kwargs):
    response = "CON Enter your preferred language:\n"
    response +="""
1. English
2. Hausa
3. Igbo
4. Yoruba"""
    Ussd.create_or_update(kwargs['session_id'], 'do_update_user_language', 'start')
    return response

def update_user_password(**kwargs):
    response = "CON Enter your old password:\n"
    Ussd.create_or_update(kwargs['session_id'], 'confirm_user_password', 'start')
    return response

def confirm_user_password(**kwargs):
    password = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    if user.check_password(password):
        response = "CON Enter new password:\n"
        Ussd.create_or_update(kwargs['session_id'], 'do_change_user_password', 'update_user_password')
    else:
        response = "END Invalid old password\n"
        Ussd.create_or_update(kwargs['session_id'], 'start', 'update_user_password')
    return response

def set_user_password(**kwargs):
    response = "CON Enter new password:\n"
    Ussd.create_or_update(kwargs['session_id'], 'do_change_user_password', 'update_user_password')
    return response

def do_update_user_name(**kwargs):
    name = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    user.update(name=name)
    Ussd.create_or_update(kwargs['session_id'], 'start', 'start')
    return start(**kwargs)

def do_update_user_language(**kwargs):
    language_index = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    user.update(language=find_language_by_index(language_index).lower())
    Ussd.create_or_update(kwargs['session_id'], 'start', 'start')
    return start(**kwargs)

def find_language_by_index(index: str) -> str:
    languages = [
        "English",
        "Hausa",
        "Igbo",
        "Yoruba"
    ]
    return languages[int(index)-1]

def do_change_user_password(**kwargs):
    new_password = kwargs['selection'].split('*')[-1]
    user = kwargs['user']
    user.password = new_password
    user.hash_password()
    user.update(is_set=True)
    send_sms(user.phone, """Welcome to KnowNet
             Start by sending your first question.""")
    Ussd.create_or_update(kwargs['session_id'], 'start', 'confirm_user_password')
    return start(**kwargs)