# Бот АНО "Культура”
Бот предназначеный для описания арт-объектов, а так же сбора отзывов о них.
Можно сказать - _"проводит экскурсию по уличным инсталяциям"_


### Описание работы


При подаче команды  /start  активируется бот
Далее он покажет место входа на фестиваль.

Ну вот и подошло все к концу.

# Инструкция к запуску боту

### Заполнение evn фала.
Стоит уточнить что без него ничего не будет работать. Ведь в нем хранятся секретные переменные которые дают сцепление с самими телеграмом.
```
#Необходимо указать токен для телеграмм-бота
TELEGRAM_TOKEN=
#Необходимо указать ID чата телеграмм
TELEGRAM_CHAT_ID=
### Google
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

1) Копируем  @BotFather  и вставляем в поиск
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/7b6cbfa6-88c2-4e66-8d77-564e87f7f86d)
2) Запускаем бота и выбираем /newbot
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/bd5524ef-704f-4c40-8ac0-3373c07cdb23)
3) Пытаемся подобрать уникальное имя и юзерку (Что такое юзерка? Стоит узнать! Это короткое и уникальное имя бота/пользователя/группы формата  @ЭтоЮзерка ).
В этом мире железок есть два правила:
- бот первый не пишет пользователю
- имя должно кончаться на bot

![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/4447dc17-477e-4af9-a97d-12002478da3d)

4) После всех процедур, вам выдаст такое сообщение. Стоит обрадоваться, ведь у вас есть свой бот. Бот - ваш ребенок и надо его защитить от сглаза.
Поэтому никому не показываем то что выделено как ключ  5829707275:AAEXR6AF77cSbjqyfu46bOy0BP_9VWcMppM
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/1aedd0c6-1a44-4a93-9f70-0e4222f3fd9c)
5) Закидываем в первую константу env файла и идем разминать спину.
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/a7484b8e-c4d4-423a-b5b6-c6ae67b5b25d)


### Как узнать TELEGRAM_CHAT_ID? Этому еще в школе учили...

1) Для любителей поспать на уроках посвящается. Копируем  @getmyid_bot  и вставляем в поиск
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/7b6cbfa6-88c2-4e66-8d77-564e87f7f86d)
2) /start и все. На этом моменте бот уже будет работать
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/fc828494-7261-48e9-9a8a-9d8c9ea28788)
3) Копируем и вставляем во вторую константу TELEGRAM_CHAT_ID. И можем тестить функционал бота
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/d03c6a38-0748-424f-9ba8-cb1d69518b9c)

### Как узнать бок данных от Google? Ну ладно, только никому

Блок данных от гугла тоже должен быть в строгой секретности, иначе все узнают что и кто написал об экспонате.

1) Если вы бесстрашный воин, то преходите по этой [ссылке](https://console.cloud.google.com/projectselector2/home/dashboard)
2) Дальше все как во всех боевиках. Создаем проект, заходим во вкладку API and Servises. Создаем Google Sheets.
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/327316c8-0ec3-4311-878c-73fd9c1e330c)
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/e6e40a8f-0af1-4b06-9187-be8301669108)
3) Дальше как в квесте. По подсказкам разгадываем ребус
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/f4675e84-15b7-4fe3-b433-58265e0aaf49)
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/cf80d99a-05b3-46b2-8994-5d3aff035a15)
4) Эта форма состоит из трёх полей:
- Service account name — имя аккаунта, может быть любым;
- Service account ID — ID, формируется автоматически из имени аккаунта;
- Service account description — описание сервисного аккаунта; тут можно написать, за что будет отвечать этот сервисный аккаунт.
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/dbeddea5-5872-4ae3-9a56-a2b45630b119)
5) Где будет выбор роли - ставим Basic
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/7ceedd4b-4fa6-4a35-af2a-2f977a5a83a6)
6) Должно выйти что-то в этом духе
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/cf8461f1-c756-4c48-aa43-0925d2846cec)
#### Остался последний рывок
7) Получаем JSON-файл с ключом доступа к сервисному аккаунту
- Осталось получить JSON-файл с ключом доступа к сервисному аккаунту и можно будет отвлечься от интерфейсных дебрей Google Cloude Platform.
- Перейдите на экран Credentials, нажмите на строчку с названием вашего сервисного аккаунта, чтобы попасть в его настройки.
- Нажмите Keys – Add Key – Create New Key, чтобы создать ключ доступа к вашему сервисному аккаунту.
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/8f03275e-dc7c-43ae-8b6f-569659473ee2)
![image](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_3/assets/108357574/07433e35-bc18-483b-ac4c-caf1ae21c358)
8) Дело мастера боится. К нам скачивается JSON файл (~~не вирус~~). Если есть редакторы кода (VSCode, Noteapd++, Sublime), то открываете этот файл там, если нет то качаем и открываем. Должно быть что-то типо

```
{
"type": "service_account",
"project_id": "fluid-dreamer-343515",
"private_key_id": "47169bcc4c4......8a331d4b769eb1ff",
"private_key": "-----BEGIN PRIVATE KEY-----\n....bTxwcv\n-----END PRIVATE KEY-----\n",
"client_email": "test-praktikum@fluid-dreamer-343515.iam.gserviceaccount.com",
"client_id": "114239083367454348646",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-praktikum%40fluid-dreamer-343515.iam.gserviceaccount.com"
}
```
Теперь нам надо вставить это все в соответсвующее константы БЕЗ СКОБОЧЕК И ПРОЧЕЙ МИШУРЫ

### Как проверить что все хорошо? Пока никак

Как быть с тем что осталось? Не буду вас мучить. Копируйте и выдыхайте
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
# Если вы делаете все на удалённом сервере

### Бот к запуску готов. Осталось вставить ключ зажигание и вперед!
Шутка! Первым делом надо обновить все на ВМ
Вообще просто вставляйте в строку все что я напишу по порядку.
```
sudo apt upgrade -y
sudo apt install curl
# Эта команда скачает скрипт для установки докера
curl -fsSL https://get.docker.com -o get-docker.sh
# Эта команда запустит его
sh get-docker.sh
sudo apt remove docker docker-engine docker.io containerd runc #должно быть E: Unable to locate package docker-engine
sudo apt update
sudo apt install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-compose -y
sudo systemctl status docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo docker-compose up -d --build
```
Теперь точно тестим
