# Shortener

Сервис для тех, кому нужно сократить длинную ссылку и поделиться ею.

## Запуск

```text
Репозиторий: https://github.com/lazer361/mispisit-lab1
Pull Request: https://github.com/lazer361/mispisit-lab1/pull/2
Образ: https://hub.docker.com/r/lazer361/mispisit-lab1

docker pull lazer361/mispisit-lab1:0.0.2
docker run --rm -p 8080:8080 lazer361/mispisit-lab1:0.0.2
```

Откройте http://localhost:8080. В меню можно создать ссылку, посмотреть список и открыть пример недоступной ссылки. Записи хранятся в памяти приложения до остановки контейнера.