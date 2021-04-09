from vk_api.longpoll import VkLongPoll, VkEventType
from connections import VKBotConnection, DataBaseConnection
from database_working import check_db_master, check_user_is_in_db, \
    add_user_to_favourites, add_user_photos_to_favourites, add_to_black_list, write_bot_message
from api_interaction import search_dating_users, json_create, get_photo, sort_photos_by_likes
from bot_working import bot_get_messages, show_bot_menu, show_info, register_new_user, go_to_favourites, \
    go_to_blacklist
import database_model
from sqlalchemy.ext.declarative import declarative_base

session = DataBaseConnection().session
engine = DataBaseConnection().engine
Base = declarative_base()
vk = VKBotConnection().vk_session
longpoll = VKBotConnection().longpoll

if __name__ == '__main__':
    database_model.Base.metadata.create_all(engine)

    while True:
        msg_text, user_id = bot_get_messages()
        print('start', msg_text, user_id)

        if msg_text.lower() == 'vkinder':
            show_bot_menu(user_id)
            msg_text, user_id = bot_get_messages()
            print(msg_text, user_id)

            if msg_text.lower() == 'да':
                try:
                    if check_db_master(user_id):
                        current_user_id == check_db_master(user_id)
                    else:
                        pass
                except Exception:
                    write_bot_message(user_id, 'Вы уже зарегистрированы, введите - поиск')
                    msg_text, user_id = bot_get_messages()
                else:
                    register_new_user(user_id)
                    write_bot_message(user_id, 'Теперь введите - поиск')
                    msg_text, user_id = bot_get_messages()
            else:
                pass

            if msg_text.lower() == 'поиск':
                write_bot_message(user_id, 'Пол нового знакомого: если женщина, введите - 1, мужчина - 2, любой - 0.')
                msg_text, user_id = bot_get_messages()

                if msg_text in ['1', '2', '0']:
                    sex = int(msg_text)
                    write_bot_message(user_id, 'Укажите нижнюю границу возраста нового знакомого, например - 18')
                else:
                    write_bot_message(user_id, 'Пол введен некорректно, попробуйте еще раз')
                    break

                msg_text, user_id = bot_get_messages()

                if msg_text.isdigit():
                    age_from = int(msg_text)
                    write_bot_message(user_id, 'Укажите верхнюю границу возраста нового знакомого, например - 55')
                else:
                    write_bot_message(user_id, 'Нижняя граница возраста введена некорректно, попробуйте еще раз')
                    break

                msg_text, user_id = bot_get_messages()

                if msg_text.isdigit():
                    age_to = int(msg_text)
                    write_bot_message(user_id, 'Укажите город нового знакомого, например - Воронеж')
                else:
                    write_bot_message(user_id, 'Верхняя граница возраста введена некорректно, попробуйте еще раз')
                    break

                msg_text, user_id = bot_get_messages()

                if msg_text:
                    city = msg_text
                    write_bot_message(user_id, 'Укажите семейное положение нового знакомого:\n'
                                               '1 — не женат (не замужем)\n'
                                               '4 - женат (замужем)\n')
                else:
                    write_bot_message(user_id, 'Город введен некорректно, попробуйте еще раз')
                    break

                msg_text, user_id = bot_get_messages()

                if msg_text.isdigit():
                    status = int(msg_text)
                else:
                    write_bot_message(user_id, 'Семейное положение введено некорректно, попробуйте еще раз')
                    break

            result = search_dating_users(sex, age_from, age_to, city, status)
            current_user_id = check_db_master(user_id)

            for i in range(len(result)):
                dating_user, black_list_user = check_user_is_in_db(result[i][3])
                user_photo = get_photo(result[i][3])
                if user_photo == 'нет доступа к фото' or dating_user is not None or black_list_user is not None:
                    continue
                sorted_user_photo = sort_photos_by_likes(user_photo)
                write_bot_message(user_id, f'\n{result[i][0]}  {result[i][1]}  {result[i][2]}')

                try:
                    write_bot_message(user_id, f'фото:',
                                      attachment=','.join
                                      ([sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                                        sorted_user_photo[-3][1]]))
                except IndexError:
                    for photo in range(len(sorted_user_photo)):
                        write_bot_message(user_id, f'фото:',
                                          attachment=sorted_user_photo[photo][1])

                write_bot_message(user_id, '1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска')
                msg_text, user_id = bot_get_messages()

                if msg_text == '0':

                    if i >= len(result) - 1:
                        show_info()

                elif msg_text == '1':

                    if i >= len(result) - 1:
                        show_info(user_id)
                        break
                    try:
                        add_user_to_favourites(user_id, result[i][3], result[i][1],
                                               result[i][0], city, status, result[i][2], current_user_id.id)
                        add_user_photos_to_favourites(user_id, sorted_user_photo[0][1],
                                                      sorted_user_photo[0][0], current_user_id.id)

                        json_create(result, photos=[sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                                                    sorted_user_photo[-3][1]])

                    except AttributeError:
                        write_bot_message(user_id, 'Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота')
                    except IndexError:
                        pass

                elif msg_text == '2':

                    if i >= len(result) - 1:
                        show_info(user_id)
                    try:
                        add_to_black_list(user_id, result[i][3], result[i][1],
                                          result[i][0], city, status, result[i][2],
                                          sorted_user_photo[0][1],
                                          sorted_user_photo[0][0], current_user_id.id)
                    except IndexError:
                        pass
                elif msg_text.lower() == 'q':
                    write_bot_message(user_id, 'Введите Vkinder для активации бота')
                    break

                elif msg_text == '2':
                    go_to_favourites(user_id)
                elif msg_text == '0':
                    go_to_blacklist(user_id)
