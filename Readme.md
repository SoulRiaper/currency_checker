# Currency checker
Сервис для конвертации валюты в режиме реального времени

### Для развертывания необходимо иметь Docker и Docker-compose
## Также необходимо создать файл .env в папке [app](app)
* В нем указать ключ для доступа к api сервису валют `APIKEY=YOUR_KEY`
* IP/HOST для Redis `REDIS_HOST=YOUR_HOST`
* Port для Redis `REDIS_PORT=YOUR_PORT`

## Алгоритм развертывания
1. Клонируйте репозиторий `git clone https://github.com/SoulRiaper/currency_checker.git .`
2. Перейдите в папку приложения `cd app`
3. Создайте файл `.env` с необходимыми переменными среды
4. Перейдите в корневой каталог `cd ..`
5. Начните создание контейнеров с помощью `docker-compose up -d`