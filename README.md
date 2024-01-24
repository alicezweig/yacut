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

* Если у вас Linux/macOS
    ``` bash
    source venv/bin/activate
    ```

* Если у вас windows
    ``` bash
    source venv/scripts/activate
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

### Запуск проекта
``` bash
flask run
```

### Создать базу данных
``` bash
flask shell
```
``` python
from yacut import db
```
``` python
db.create_all()
```
``` python
exit()
```
### Создать и применить миграции
``` bash
flask db init
```
``` bash
 flask db migrate -m "initial"
```

## API Yacut
См. redoc.html
