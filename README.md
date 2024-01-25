# Yacut - сервис укоротитель ссылок + API

**Проект выполнен** Yandex Практикум и [Ирина Иванова](https://github.com/alicezweig)

## Технологии
    Python
    Flask

## Возможности 
- генерация  коротких ссылок и связь их с исходными длинными ссылками
- переадресация на исходный адрес при обращении к коротким ссылкам

### Клонировать репозиторий и перейти в него в командной строке:
``` bash
    sudo apt update && sudo apt upgrade
```
``` bash
    git clone https://github.com/alicezweig/scrapy_parser_pep.git ./yacut
```
``` bash
    cd yacut
```

### Cоздать и активировать виртуальное окружение:
``` bash
    python3 -m venv venv
```
``` bash
source venv/bin/activate
```

### Установить зависимости из файла requirements.txt:
``` bash
python3 -m pip install --upgrade pip
```
``` bash
pip install -r requirements.txt
```

### Заполнить файл с переменными окружения (см. .env.example)
``` bash
touch .env && nano .env
```

### Создать базу данных и применить миграции
``` bash
flask db upgrade
```

### Запуск проекта
``` bash
flask run
```

### API Yacut
[Документация](https://petstore.swagger.io/?url=https://github.com/alicezweig/yacut/blob/master/redoc.html)

