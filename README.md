# Shortener

Сервис для тех, кому нужно сократить длинную ссылку и поделиться ею.
На странице «Состояние» видно, доступна ли база и какая короткая ссылка создана последней.

## Запуск

```text
Репозиторий: https://github.com/lazer361/mispisit-lab1
Ветка: lab5
Pull Request: https://github.com/lazer361/mispisit-lab1/pull/5
Образ: lazer361/mispisit-lab1:0.0.5

git clone -b lab5 https://github.com/lazer361/mispisit-lab1
cd mispisit-lab1
docker compose up -d
```

Откройте http://localhost:8080 и перейдите в «Состояние». До создания первой ссылки в версии 0.0.5 событий нет. Создайте ссылку через форму и вернитесь на страницу состояния. Появятся название ссылки, короткий код и время создания.