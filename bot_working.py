from vk_api.longpoll import VkLongPoll, VkEventType
from connections import VKBotConnection
from database_working import check_users_are_in_favourites, delete_user_from_favorites, check_users_are_in_black_list,\
    delete_user_from_black_list, register_user, write_bot_message

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



