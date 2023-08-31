# Бот АНО "Культура”
Бот предназначеный для описания арт-объектов, а так же сбора отзывов о них.
Можно сказать - _"проводит экскурсию по уличным инсталяциям"_


### Описание работы 


При подаче команды `/start` активируется бот. Он сразу вас попревествует.
Далее он покажет место входа на фестиваль. 

Ну вот и подошло все к концу. 

# Инструкиция к запуску боту

### Заполнение evn фала.
Стоит уточнить что без него ничего не будет работать. Ведь в нем храняться секретыне переменные которые дают сцепление с самими телеграмом.
```
#Необходимо указать токен для телеграмм-бота
TELEGRAM_TOKEN=
#### Необходимо указаь ID чата телеграмм
TELEGRAM_CHAT_ID=
# Google
EMAIL=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
# Указываем базу данных
DB_ENGINE=
# Указываем имя базы данных
DB_NAME=
# Указываем логин для подключения к базе данных
POSTGRES_USER=
# Указываем пароль для подключения к базе данных
POSTGRES_PASSWORD=
# Указываем название сервиса (контейнера) с базой данных
DB_HOST=
# Указываем порт для подключения к базе даннах
DB_PORT=
```
### Как узнать токен бота TELEGRAM_TOKEN? Первым делом нужно его создать!

1) Копирукем `@BotFather` и вставляем в поиск 
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/7b6cbfa6-88c2-4e66-8d77-564e87f7f86d)
2) Запускаем бота и выбираем /newbot
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/bd5524ef-704f-4c40-8ac0-3373c07cdb23)
3) Пытаемся подобрать уникальное имя и юзерку (Что такое юзерка? 🥶🥶🥶 стоит узнать! Это которкое и уникальное имя бота/пользователя/группы формата `@ЭтоЮзерка`).
В этом мире железок есть два правила:
   - бот первый не пишет пользователю
   - имя должно кончаться на bot
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/4447dc17-477e-4af9-a97d-12002478da3d)
4) После всех процедур, вам выдат такое сообщение. Стоит обрадоваться, ведь у вас есть свой бот.
Бот - ваш ребенок и надо его защитить от сглаза.
Поэтому никому не показываем то что выделено как ключ `5829707275:AAEXR6AF77cSbjqyfu46bOy0BP_9VWcMppM`
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/1aedd0c6-1a44-4a93-9f70-0e4222f3fd9c)
5) Закидываем в первую константу env файла и идем разминать спину.
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/a7484b8e-c4d4-423a-b5b6-c6ae67b5b25d)


### Как узнать TELEGRAM_CHAT_ID? Этому еще в школе учили...

1) Для любетелей поспать на уроках посвящается. Копируем `@getmyid_bot` и вставялем в поиск
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/7b6cbfa6-88c2-4e66-8d77-564e87f7f86d)
2) /start и все. На этом моменте бот уже будет работать
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/fc828494-7261-48e9-9a8a-9d8c9ea28788)
3) Копируем и вставляем во вторую константу TELEGRAM_CHAT_ID












