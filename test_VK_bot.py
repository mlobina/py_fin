import pytest
from VK_searching_methods import search_dating_users, get_photo, sort_photos_by_likes
from VK_BD_interaction_methods import register_user, add_user_to_favourites,\
    add_user_photos_to_favourites, add_to_black_list

class TestBot:

    def setup_class(self):
        print('method setup_class')

    def setup(self):
        print('method setup')

    def teardown(self):
        print('method teardown')

    @pytest.mark.parametrize('sex, age_at, age_to, city, status, result', [
            ('1', '18', '20', 'Москва', '1', True)])
    def test_search_dating_users(self, sex, age_at, age_to, city, status, result):
        assert search_dating_users(sex, age_at, age_to, city, status) == result


    @pytest.mark.parametrize('user_id, result', [('336261034', True)])
    def test_get_photo(self, user_id, result):
        assert get_photo(user_id) == result


    @pytest.mark.parametrize('list_photos, result',
                                 [(['1', 'photo_1', '2', 'photo_2', '3', 'photo_3'],
                                   ['1', '2', '3', 'photo_1', 'photo_2', 'photo_3']), ])
    def test_sort_photos_by_likes(self, list_photos, result):
        assert sort_photos_by_likes(list_photos) == result


    @pytest.mark.parametrize('vk_id, result', [('1', False), ('1', False), ('627970171', False)])
    def test_register_user(self, vk_id, result):
        assert register_user(vk_id) == result


    @pytest.mark.parametrize('event_id, vk_id, first_name, second_name, city, status, link, id_user, result',
                             [('2323231', '2', 'gogol', 'mogol', 'Rusco', '2', 'www.rt.ru', '1', False)])
    def test_add_user_to_favourites(self, event_id, vk_id, first_name, second_name, city, status,  link, id_user, result):
        assert add_user_to_favourites(event_id, vk_id, first_name, second_name, city, status, link, id_user) == result


    @pytest.mark.parametrize('event_id, link_photo, count_likes, id_dating_user, result',
                             [('111', 'my_link', '100', '1233211', False)])
    def test_add_user_photos_to_favourites(self, event_id, link_photo, count_likes, id_dating_user, result):
        assert add_user_photos_to_favourites(event_id, link_photo, count_likes, id_dating_user) == result


    @pytest.mark.parametrize(
        'event_id, vk_id, first_name, second_name, city, status, link, link_photo, count_likes, id_user, result',
        [('123', '12', '12434', '1251231', 'sdfsdfs', 'aaa', 'sfsdfsdfds', 'fsdfsdfs', '12', '123', False)])
    def test_add_to_black_list(self, event_id, vk_id, first_name, second_name, city, status, link, link_photo, count_likes,
                                    id_user, result):
        assert add_to_black_list(event_id, vk_id, first_name, second_name, city, status, link, link_photo, count_likes,
                                 id_user) == result

    def teardown_class(self):
        print('method teardown_class')

