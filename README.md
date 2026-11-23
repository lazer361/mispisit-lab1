# Shortener

Сервис для тех, кому нужно сократить длинную ссылку и поделиться ею.

## Запуск

```text
Репозиторий: https://github.com/lazer361/mispisit-lab1
Ветка: lab3
Pull Request: https://github.com/lazer361/mispisit-lab1/pull/3
Образ: lazer361/mispisit-lab1:0.0.3
Страница образа: https://hub.docker.com/r/lazer361/mispisit-lab1

git clone -b lab3 https://github.com/lazer361/mispisit-lab1
cd mispisit-lab1
docker compose up -d
```

Откройте http://localhost:8080. При первом запуске список пустой. Создайте ссылку и пересоздайте контейнеры командами `docker compose down` и `docker compose up -d`. Ссылка останется в списке, потому что PostgreSQL хранит данные в томе `dbdata`.