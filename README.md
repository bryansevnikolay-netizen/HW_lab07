## Лабораторная работа по работе с docker

## Домашнее задание

В репозитории приведен код web-приложения, которое сохраняет в БД введенную информацию о задаче - ее имя.

## Часть I. Docker

1. Добавьте в код Dockerfile, который позволит запустить web-приложение с исходным кодом в каталоге app/ через docker.
```
FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 5000
CMD ["python", "app.py"]
```
2. Выполните запуск контейнера с этим приложением.
```
docker build -t task-app .
docker exec -it task-db mysql -uroot -prootpass -e "USE taskdb; SELECT * FROM items;"
```
Вывод:
```
+----+-----------+
| id | name      |
+----+-----------+
|  1 | Пример 1  |
|  2 | Пример 2  |
+----+-----------+
```
3. Скопируйте из консоли в каталог /home/ контейнера файл README.md.
```
docker cp README.md my-task-app:/home/
```
4. Подключитесь к терминалу контейнера с приложением в интерактивном режиме. Проверьте, что скопированный файл находится в нужном каталоге.
```
docker exec -it my-task-app bash
cd /home
ls
cat README.md
pwd
```
5. Выйдите из интерактивного режима.
```
exit
```  
6. Остановите контейнер с приложением.
```
docker stop my-task-app && docker rm my-task-app
```

## Часть II. Docker compose
1. Создайте файл docker-compose.yml таким образом, чтобы совместно с описанным в части 1 контейнером работала бы база данных mysql. Файл инициализации БД в каталоге db/init.sql. Также пропишите порт подключения к приложению. Например 5000.
```
services:
  db:
    image: mariadb:10.11
    container_name: task-db
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: taskdb
      MYSQL_USER: taskuser
      MYSQL_PASSWORD: taskpass
    volumes:
      - ./deb/init.sql:/docker-entrypoint-initdb.d/init.sql
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"
  web:
    build: .
    container_name: my-task-app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: taskuser
      DB_PASSWORD: taskpass
      DB_NAME: taskdb
    depends_on:
      - db

volumes:
  db_data:
```
2. Запустите связку web-приложение - БД.
```
docker compose up -d
```
3. Проверьте подключение к приложению через браузер. Сделайте снимок экрана.
(снимок экрана приложен к файлаи репозитория)
4. Проверьте работу приложения через браузер.
   1) Добавление 1-ой задачи "New goal!"
   2) Добавление 2-ой задачи "Victory!!!"
Вывод обновленного содержимого через терминал:
```
+----+-------------------------+
| id | name                    |
+----+-------------------------+
|  1 | Пример 1                |
|  2 | Пример 2                |
|  3 | New goal!               |
|  4 | Victory!!!              |
+----+-------------------------+
```
(снимок экрана с результатами приложен к файлаи репозитория)

