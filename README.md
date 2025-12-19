#ТЗ

Автоматизированные UI-тесты авторизации для сайта  
https://www.saucedemo.com/

## Стек
- Python 3.11.9
- Playwright 1.55.0
- Pytest
- Allure 2.36.0
- Docker 29.1.3
- Page Object pattern

## Покрытые сценарии
1. Успешный логин (`standard_user / secret_sauce`)
2. Логин с неверным паролем
3. Логин заблокированного пользователя (`locked_out_user`)
4. Логин с пустыми полями (username/password)
5. Логин пользователя `performance_glitch_user`  
   (проверка корректного перехода несмотря на задержки)
   
## Требования
- Использовать Selenium или Playwright
- Использовать Page Object
- Подключить Allure
- Проверять корректность URL и отображение элементов
- Добавить Dockerfile для запуска тестов в контейнере
- Python
- Все зависимости - в requirements.txt
- Короткая инструкция по запуску - в README.md

## Установка и запуск (локально, Windows)

### 1. Клонировать репозиторий и перейти в папку проекта
```
cd ...:\...
```
### 2. Создать и активировать виртуальное окружение
```
python -m venv .venv

.venv\Scripts\activate
```
### 3. Установить зависимости
```
pip install -r requirements.txt
```
### 4. Установить браузеры Playwright
```
python -m playwright install --with-deps
```
### 5. Запуск тестов
```
pytest
```
### 6. Запуск в headed-режиме
```
pytest --headed
(Можно и без "--headed")
```
### 7. Результаты Allure автоматически сохраняются в папку allure-results. Просмотр отчёта
```
allure serve allure-results
```
### 8. Запуск тестов в Docker. Сборка Docker-образа
```
docker build -t tz_aqa .
```
### 9. Запуск тестов в контейнере
```
docker run --rm -v "%cd%\allure-results:/app/allure-results" tz_aqa
```
### 10. После выполнения тестов Allure-отчёт можно открыть локально
```
allure serve allure-results
```