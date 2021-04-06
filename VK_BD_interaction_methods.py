
from vk_api.utils import get_random_id
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from VK_DB_connections import VKBotConnection, DataBaseConnection
from DB_model import User, DatingUser, Photos, BlackList

vk = VKBotConnection().vk_session
Session = DataBaseConnection().session
engine = DataBaseConnection().engine
session = Session()

def write_bot_message(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id(), 'attachment': attachment})


def register_user(vk_id):
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        return True
    except(IntegrityError, InvalidRequestError):
        return False


def check_DB_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


def check_user_is_in_DB(ids):
    dating_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    black_list_user = session.query(BlackList).filter_by(vk_id=ids).first()
    return dating_user, black_list_user


def add_user_to_favourites(event_id, vk_id, first_name, last_name, city, status, link, id_user):
    try:
        new_user = DatingUser(vk_id=vk_id,
                              first_name=first_name,
                              last_name=last_name,
                              city=city,
                              status=status,
                              link=link,
                              id_user=id_user)
        session.add(new_user)
        session.commit()
        write_bot_message(event_id, 'Пользователь добавлен в Избранное')
        return True
    except(IntegrityError, InvalidRequestError):
        write_bot_message(event_id, 'Пользователь уже есть в Избранном')
        return False


def check_users_are_in_favourites(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    all_users_favourites = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
    return all_users_favourites



def delete_user_from_favorites(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


def add_user_photos_to_favourites(event_id, link_photo, count_likes, id_dating_user):
    try:
        new_user = Photos(link_photo=link_photo,
                          count_likes=count_likes,
                          id_dating_user=id_dating_user)
        session.add(new_user)
        session.commit()
        write_bot_message(event_id, 'Фото пользователя добавлено в Избранное')
        return True
    except(IntegrityError, InvalidRequestError):
        write_bot_message(event_id, 'Фото пользователя уже есть в Избранном')
        return False


def add_to_black_list(event_id, vk_id, first_name, last_name, city, status, link,
                      link_photo, count_likes, id_user):
    try:
        new_user = BlackList(vk_id=vk_id,
                             first_name=first_name,
                             last_name=last_name,
                             city=city,
                             status=status,
                             link=link,
                             link_photo=link_photo,
                             count_likes=count_likes,
                             id_user=id_user)
        session.add(new_user)
        session.commit()
        write_bot_message(event_id, 'Пользователь добавлен в "черный список"')
        return True
    except(IntegrityError, InvalidRequestError):
        write_bot_message(event_id, 'Пользователь уже есть в "черном списке"')
        return False


def check_users_are_in_black_list(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    all_users_black_list = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
    return all_users_black_list

def delete_user_from_black_list(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

