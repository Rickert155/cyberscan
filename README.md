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
from cyberwarn.core.header import Headers

# Можно использовать параметр create_new_agent со значением True
# для обновления заголовков в json
headers = Headers().create_headers(create_new_agent=False) 
```

## Использование модулей
Можно использовать CLI, для этого следует запустить основной модуль
```sh
python3 -m cyberscan
```
Результат будет примерно такой:
```sh
|--------------------------------------------------------
| author:       CyberWarn	https://gitea.com/cyberwarn
| project:      CyberScan	GPLv3      
| version:      0.1     
|--------------------------------------------------------
|   CyberScan
|   [1] Сканер плагинов WordPress
|   [2] Определить CMS
| >>> 
```

## Сканер плагинов WordPress
Можно использовать аргументы командной строки:
```sh
python3 -m cyberscan wp-plugins https://127.0.0.1:3000
```
Можно использовать как модуль:
```sh
python3 -m cyberscan.cms.wp_plugins --url=https://127.0.0.1:3000
```
## Сканер версии WordPress
```sh
python3 -m cyberscan wp-version http://127.0.0.1:3000
```
```sh
python3 -m cyberscan.cms.wp_version url=http://127.0.0.1:3000
```

## Сканер поддоменов
> Для сканирования поддоменов необходимо указать URL и путь к wordlist для перебора(в инструмент добавлены тестовые вордлисты data/wordlist)
Использование аргументов командной строки
```sh
python3 -m cyberscan fuzz_subdomains https://example.com data/wordlist/web/subdomains.txt
```
Использование, как модуля:
```sh
python3 -m cyberscan.fuzz.fuzz_subdomain --url="https://example.com" --wordlist=data/wordlist/web/subdomains.txt
```
