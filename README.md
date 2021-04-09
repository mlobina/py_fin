# Дипломная работа


## VKinder
Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок.

Используя данные из VK нужно сделать сервис намного лучше чем Tinder. Искать людей, подходящих под условия, на основании информации о пользователе из VK:
- возраст,
- пол,
- город,
- семейное положение.

У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии с аватара. Популярность определяется по количеству лайков и комментариев.


## Запуск программы  
Для начала работы программы необходимо создать:
 - базу данных в PostgreSQL;
 - файл .env по аналогии с файлом env_example и передать в него токен сообщества, в котором будет работать бот, токен пользователя, для которого осуществляется поиск, и DSN базы данных;  
 - начало работы программы осуществляется при запуске модуля run.py.
  
Для активации бота VKinder необходимо написать сообщение VKinder в сообщество со страницы пользователя. Далее бот попросит пройти регистрацию и приступить к поиску, передав ему необходимые параметры.  
Пользователь может ознакомиться с предложенными ботом кандидатурами для знакомства и передать их дибо в Избранное, либо в "Черный сптсок". Избранное отображается в файле result.json.