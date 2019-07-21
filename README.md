# Cyberarena API

Документ описывает структуру запросов для доступа к API сети компьютерных клубов CyberArena.



## **Кейсы**

#### **Все кейсы**

| Эндпоинт                   | /shop/cases |
| :------------------------- | ----------- |
| **Метод**                  | GET         |
| ***Требует access_token*** |             |

Результат запроса

```json
{
    "cases": [
        {
            "description": "Скидки на покупку времени",
            "name": "Скидки",
            "id": 1
        }
    ]
}
```

#### **Определенный кейс**

| Эндпоинт                   | /shop/cases/\<int:id\> |
| :------------------------- | ---------------------- |
| **Метод**                  | GET                    |
| ***Требует access_token*** |                        |

Результат запроса

~~~json
{
    "case": {
        "description": "Скидки на покупку времени",
        "name": "Скидки",
        "id": 1
    },
    "items": [
        {
            "name": "Скидка на игру за ПК",
            "probability": 0.1,
            "description": "Скидка 20%",
            "expiration_period": 3600,
            "case": 1,
            "id": 1
        },
        {
            "name": "Скидка на игру за консолью",
            "probability": 0.7,
            "description": "Скидка 30%",
            "expiration_period": 3600,
            "case": 1,
            "id": 2
        },
        {
            "name": "Скидка на игру за ПК",
            "probability": 0.2,
            "description": "Скидка 30%",
            "expiration_period": 3600,
            "case": 1,
            "id": 3
        }
    ]
}
~~~

**Все предметы пользователя**

| Эндпоинт                   | /shop/items |
| :------------------------- | :---------- |
| **Метод**                  | GET         |
| ***Требует access_token*** |             |

Результат запроса

```json
{
    "items": [
        {
            "code": null,
            "id": 20,
            "expiration": null,
            "item": {
                "name": "Скидка на игру за консолью",
                "probability": 0.7,
                "description": "Скидка 30%",
                "expiration_period": 3600,
                "case": 1,
                "id": 2
            }
        }
    ]
}
```

#### **Открыть кейс**

| Эндпоинт                   | /shop/cases/\<int:id\> |
| :------------------------- | ---------------------- |
| **Метод**                  | POST                   |
| ***Требует access_token*** |                        |

```json
{
    "reward": {
        "name": "Скидка на игру за консолью",
        "description": "Скидка 30%",
        "case": 1,
        "expiration_period": 3600,
        "id": 2,
        "probability": 0.7
    }
}
```

#### **Активировать предмет**

| Эндпоинт                   | /shop/items/\<int:id\> |
| :------------------------- | :--------------------- |
| **Метод**                  | PATCH                  |
| ***Требует access_token*** |                        |

```json
{
    "item_id": 20,
    "code": "K73TM",
    "expires_in": 3599.774419
}
```

## **Новости**

#### **Все новости**

| Эндпоинт                 | /news |
| :----------------------- | :---- |
| **Метод**                | GET   |
| **Требует access_token** |       |

Параметры

| offset | Позволяет отступить от начала несколько новостей     |
| ------ | ---------------------------------------------------- |
| count  | Колчество новостей, которое должен возвратить сервер |

Пример запроса /news?offset=5&count=3

```json
{
    "news": [
        {
            "date": 1473941545,
            "text": "Ребята, вчера получила информацию, оповещаю Вас.",
            "attachments": []
        },
        {
            "date": 1473953059,
            "text": "26.09.16 у нас будет диагностическое интернет-тестирование по математике. в 15.30 в 406 каб. 10 корпуса.\nвсем быть обязательно!??",
            "attachments": []
        },
        {
            "date": 1474391197,
            "text": "???мы молодцы!",
            "attachments": [
                {
                    "id": 434838814,
                    "date": 1474391197,
                    "text": "",
                    "sizes": [
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7a/ydhzGOcThdk.jpg",
                            "type": "m",
                            "width": 130,
                            "height": 97
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7e/hMDQNVcBjkg.jpg",
                            "type": "o",
                            "width": 130,
                            "height": 98
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7f/raXIKQB5YNk.jpg",
                            "type": "p",
                            "width": 200,
                            "height": 150
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b80/E9fmJw6yerY.jpg",
                            "type": "q",
                            "width": 320,
                            "height": 240
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b81/vsVj2x90kmo.jpg",
                            "type": "r",
                            "width": 510,
                            "height": 383
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b79/dlXkQzYkK08.jpg",
                            "type": "s",
                            "width": 75,
                            "height": 56
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7b/fdj5jlF7Thw.jpg",
                            "type": "x",
                            "width": 604,
                            "height": 453
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7c/AFsoM9Yp_Dk.jpg",
                            "type": "y",
                            "width": 807,
                            "height": 605
                        },
                        {
                            "url": "https://pp.userapi.com/c837125/v837125174/b7d/hUPtwNT-yO0.jpg",
                            "type": "z",
                            "width": 1280,
                            "height": 960
                        }
                    ],
                    "post_id": 10,
                    "user_id": 100,
                    "album_id": -7,
                    "owner_id": -128373900,
                    "access_key": "51d9d7050590468f87"
                }
            ]
        }
    ]
}
```



## **Пользователь**

#### **Профиль**

| Эндпоинт                 | /user/profile |
| :----------------------- | :------------ |
| **Метод**                | GET           |
| **Требует access_token** |               |

#### **Обновить токен**

| Эндпоинт                  | /user/token_refresh |
| :------------------------ | :------------ |
| **Метод**                 | GET           |
| **Требует refresh_token** |               |

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjMzNTYxNDAsIm5iZiI6MTU2MzM1NjE0MCwianRpIjoiMDcyNDRmOGQtMWM3Mi00NjExLWE2MGItNmZkZWM2NjEzOWUxIiwiZXhwIjoxNTYzMzU3MDQwLCJpZGVudGl0eSI6IjQ2MzM3ODU0IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.3dOIjWC4pRrdbjwRQ9JnQ0luls2rC6J8rTDCwjf_qME"
}
```


