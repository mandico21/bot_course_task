# Финальное задание по курсу

Бот для телеграм-магазина, использует Inline Mode

Написан на [Aiogram](https://github.com/aiogram/)                                      
База данных: PostgreSQL                                               
ORM: SqlAlchemy
## Установка и запуск
```
git clone https://github.com/mandico21/course_task.git
```
Переименовать `.env.dist` в `.env`

### Настройка файла .env
1. Указать в `BOT_TOKEN` токен бота, токен можно получить тут [@BotFather](https://t.me/botfather)
2. Указать свой Telegram id в `ADMINS`, получить можно тут [@my_id_bot](https://t.me/my_id_bot)
3. В `TECH_GROUPS` укажите id группы, для обратной связи
4. В `PG_PASSWORD` `DB_PASS` `DB_NAME` необходимо придумать и указать пароли и имя для базы данных
5. В `QIWI` указать токен Qiwi, получить можно тут [Token](https://qiwi.com/api)
6. В `WALLET` нужно указать номер Qiwi кошелька
7. В `QIWI_P_SICRET` нужно указать секретный токен, получить можно тут [Secret_token](https://qiwi.com/p2p-admin/transfers/api)

### Запуск
```
sudo docker-compose up
```

## В Боте

```
Пропиште /start, затем /appoint_admin
```
