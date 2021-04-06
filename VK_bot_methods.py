from vk_api.longpoll import VkLongPoll, VkEventType
from VK_DB_connections import VKBotConnection
from VK_BD_interaction_methods import write_bot_message, check_users_are_in_favourites, delete_user_from_favorites, \
    check_users_are_in_black_list, delete_user_from_black_list, register_user, check_DB_master, check_user_is_in_DB, \
    add_user_to_favourites, add_user_photos_to_favourites, add_to_black_list
from VK_searching_methods import search_dating_users, json_create, get_photo, sort_photos_by_likes

vk = VKBotConnection().vk_session
longpoll = VKBotConnection().longpoll


def bot_get_messages():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


def show_bot_menu(user_id):
    write_bot_message(user_id,
                      f'Доброго времени суток! Спасибо, что используете бот VKinder для поиска новых друзей!\n'
                      f'Для начала нужно зарегистрироваться.\n'
                      f'\n Для регистрации введите  - да\n'
                      f'Если Вы уже зарегистрировались, введите - поиск\n'
                      f'Для перехода в Избранное нажмите введите - 2\n'
                      f'Для перехода к "черному списку" введите - 0\n')


def show_info(user_id_num=None):
    write_bot_message(user_id_num,
                      f'Это последняя анкета.'
                      f'Перейти в Избранное - 2'
                      f'Перейти к "черному списку" - 0'
                      f'Меню бота VKinder')


def register_new_user(user_id_num):
    write_bot_message(user_id_num,
                      f'Вы прошли регистрацию.')
    register_user(user_id_num)


def go_to_favourites(ids):
    all_users_favourites = check_users_are_in_favourites(ids)
    write_bot_message(ids, f'Избранные анкеты:')

    for nums, users in enumerate(all_users_favourites):
        write_bot_message(ids, f'{users.first_name}, {users.last_name}, {users.link}')
        write_bot_message(ids, '1 - Удалить из Избранного, 0 - Далее \nq - Выход')
        msg_texts, user_ids = bot_get_messages()

        if msg_texts == '0':
            if nums >= len(all_users_favourites) - 1:
                write_bot_message(user_ids, f'Это последняя анкета.\n'
                                            f'Vkinder - вернуться в меню\n')
        elif msg_texts == '1':
            delete_user_from_favorites(users.vk_id)
            write_bot_message(user_ids, f'Анкета успешно удалена.')
            if nums >= len(all_users_favourites) - 1:
                write_bot_message(user_ids, f'Это последняя анкета.\n'
                                            f'Vkinder - вернуться в меню\n')
        elif msg_texts.lower() == 'q':
            write_bot_message(ids, 'Vkinder - для активации бота.')
            break


def go_to_blacklist(ids):
    all_users_black_list = check_users_are_in_black_list(ids)
    write_bot_message(ids, f'Анкеты в "чёрном списке":')

    for num, user in enumerate(all_users_black_list):
        write_bot_message(ids, f'{user.first_name}, {user.second_name}, {user.link}')
        write_bot_message(ids, '1 - Удалить из "чёрного списка", 0 - Далее \nq - Выход')
        msg_texts, user_ids = bot_get_messages()
        if msg_texts == '0':
            if num >= len(all_users_black_list) - 1:
                write_bot_message(user_ids, f'Это последняя анкета.\n'
                                            f'Vkinder - вернуться в меню\n')

        elif msg_texts == '1':
            print(user.id)
            delete_user_from_black_list(user.vk_id)
            write_bot_message(user_ids, f'Анкета успешно удалена')
            if num >= len(all_users_black_list) - 1:
                write_bot_message(user_ids, f'Это последняя анкета.\n'
                                            f'Vkinder - вернуться в меню\n')
        elif msg_texts.lower() == 'q':
            write_bot_message(ids, 'Vkinder - для активации бота.')
            break


if __name__ == '__main__':
    while True:
        msg_text, user_id = bot_get_messages()
        print('start', msg_text, user_id)

        if msg_text.lower() == 'vkinder':
            show_bot_menu(user_id)
            msg_text, user_id = bot_get_messages()
            print(msg_text, user_id)

            if msg_text.lower() == 'да':
                try:
                    if check_DB_master(user_id):
                        current_user_id == check_DB_master(user_id)
                    else:
                        pass
                except:
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
            print(result)
            #json_create(result)
            current_user_id = check_DB_master(user_id)

            for i in range(len(result)):
                dating_user, black_list_user = check_user_is_in_DB(result[i][3])
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
