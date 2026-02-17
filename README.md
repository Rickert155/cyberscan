# Сканнер веб-приложений

## Клонирование/Установка
clone
```sh
git clone https://gitea.com/cyberwarn/cyberscan && cd cyberscan
```
установка пакетов
```sh
python3 -m venv venv && source venv/bin/activate && pip install -r packages.txt
```
Тестовый запуск
```sh
python3 -m cyberscan
```

## Тестирование/отладка
Подготовлен модуль header для генерирования новых HTTP заголовков. Тестирование:
```sh
python3 -m tests.headers
```
Для работы из другого модуля можно необходимо импорторовать класс Headers из модуля header и вызвать метод create_headers 
```python3
from .header import Headers

# Можно использовать параметр create_new_agent со значением True
# для обновления заголовков в json
headers = Headers().create_headers(create_new_agent=False) 
```

