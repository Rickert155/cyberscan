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

## Возможности
- Проверка поддоменов  
- Перебор директий файлов
- Сбор ссылок с ресурса
- Сбор комментариев HTML с ресурса

**Social**
- Проверка по username на различных сервисах(в процессе разработки)

**CMS**
- Сканирование плагинов WordPress
- Проверка версии WordPress

## Тестирование/отладка
Подготовлен модуль header для генерирования новых HTTP заголовков. Тестирование:
```sh
python3 -m tests.headers
```
Для работы из другого модуля необходимо импорторовать класс Headers из модуля header и вызвать метод create_headers 
```python3
from cyberwarn.core.header import Headers
# Можно использовать параметр create_new_agent со значением True
# для обновления заголовков в json
headers = Headers().create_headers(create_new_agent=False) 
```
Для теста всех модулей можно использовать tests.check_all_modules:
```sh
python3 -m tests.check_all_modules
```
Так же можно добавить произвольный URL для тестирования:
```sh
python3 -m tests.check_all_modules https://example.com
```

## Использование модулей
Можно использовать CLI, для этого следует запустить основной модуль
```sh
python3 -m cyberscan
```
Результат будет примерно такой:
```sh
|-----------------------------------------------------------------------------------
| author:       CyberWarn	https://gitea.com/cyberwarn
| project:      CyberScan	GPLv3      
| version:      0.1.2     
|-----------------------------------------------------------------------------------
|   CyberScan
|
|   [1] Поиск поддоменов: fuzz_subdomain
|   [2] Поиск файлов/директорий: fuzz_dirs
|   [3] Поиск ссылок на странице: get_links
|   [4] Поиск комментариев HTML: get_comments
|
|   Social
|   [5] Поиск по username: username(в процессе разработки)
|
|   CMS
|   [6] Сканер плагинов WordPress: wp-plugins
|   [7] Определить версию WordPress: wp-version
| >>> 
```

### Сканер плагинов WordPress
Можно использовать аргументы командной строки:
```sh
python3 -m cyberscan wp-plugins --url=https://127.0.0.1:3000
```
### Сканер версии WordPress
```sh
python3 -m cyberscan wp-version --url=http://127.0.0.1:3000
```

### Сканер поддоменов
> Для сканирования поддоменов необходимо указать URL и путь к wordlist для перебора(в инструмент добавлены тестовые вордлисты data/wordlist)
Использование аргументов командной строки
```sh
python3 -m cyberscan fuzz_subdomains --url=https://example.com --wordlist=data/wordlist/web/subdomains.txt
```

### Сканер директорий
```sh
python3 -m cyberscan fuzz_dirs --url=https://example.com --wordlist=data/wordlist/web/dir.txt
```

### Сборщик ссылок
> Больше вспомогательный модуль. Вероятно, в дальнейшем будет использоваться более серьезным модулем. На момент написания модуля была одна цель: написать сборщик ссылок для прохождения CTF на платформах.
Пример использования аргументов CLI:
```sh
python3 -m cyberscan get_links --url=http://example.com
```
### Сборщик комментариев
> Так же вспомогательный модель, как get_links  

Пример использования аргументов CLI:
```sh
python3 -m cyberscan get_comments --url=https://example.com
```

## Запуск в контейнере
Для запуска в контенере подготовлен Containerfile.  
Собираем образ:
```sh
podman build -t cyberscan -f Containerfile
```
Запускаем контейнер на основе нашего образа, монтируя директорию data:
```sh
podman run --rm -it -v $PWD/data:/root/cyberscan/data cyberscan
```
> Образ собирается вместе с vim и fish для комфортной работы в контейнере
