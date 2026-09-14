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
- Перебор директорий и файлов
- Сканирование плагинов WordPress
- Проверка версии WordPress
- Сбор ссылок с ресурса
- Сбор комментариев HTML с ресурса  
- Brute Force доступов пользователей к веб-приложению
- Поиск пользователей по нику в социальных сетях(в процессе разработки)

> Есть возможность добавить прокси в *data/settings.json*

## Тестирование/отладка
Для проверки всех модулей использовается tests/check_all_modules
```sh
python3 -m tests.check_all_modules
```
Так же можно добавить произвольный URL для тестирования:
```sh
python3 -m tests.check_all_modules https://example.com
```

## Использование модулей
Для просмотра доступных модулей использовать cyberscan без аргументов
```sh
python3 -m cyberscan
```
Вывод будет примерно таким:
```sh
|-------------------------------------------------------
| author:       CyberWarn	https://gitea.com/cyberwarn
| project:      CyberScan	GPLv3      
| version:      0.2.5     
|-------------------------------------------------------
| CyberScan
| [1] Сканер поддоменов: fuzz-subdomains
| [2] Сканер директорий: fuzz-dirs
| [3] Сборщик ссылок: get-links
| [4] Сборщик комментариев: get-comments
| [5] Сканер плагинов WordPress: wp-plugins
| [6] Сканер версии WordPress: wp-version
| [7] Брутфорс логина/пароля: bruteforce-login
| [8] Search for users on social networks: search-user
Для просмотри с примерами команд:
```sh
python3 -m cyberscan --help
```

### Сканер плагинов WordPress
Пример использования:
```sh
python3 -m cyberscan wp-plugins --url=https://127.0.0.1:3000 --workers=20
```
### Сканер версии WordPress
Пример использования:
```sh
python3 -m cyberscan wp-version --url=http://127.0.0.1:3000
```

### Сканер поддоменов
Пример использования:
```sh
python3 -m cyberscan fuzz-subdomains --url=https://example.com --wordlist=data/wordlist/web/subdomains.txt --workers=20
```

### Сканер директорий
```sh
python3 -m cyberscan fuzz-dirs --url=https://example.com --wordlist=data/wordlist/web/dir.txt --workers=20
```

### Сборщик ссылок
Пример использования:
```sh
python3 -m cyberscan get-links --url=http://example.com
```
### Сборщик комментариев
Пример использования:
```sh
python3 -m cyberscan get-comments --url=https://example.com
```

### Перебор логинов/паролей веб-приложения
Пример использования:
```sh
python3 -m cyberscan bruteforce-login --url=https://example.com/login --users=data/wordlist/users.txt --passwords=data/wordlist/auth/passwords.txt --form="username=[USER]&password=[PASSWORD]" --fm="Invalid username or password."
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

## Готовый образ Podman/Docker
Подтягиваем себе образ
```sh
podman pull ghcr.io/rickert155/cyberscan:0.2.2
```
Так же вы можете брать образ из Docker Hub
```sh
podman pull docker.io/cyberwarn/cyberscan:0.2.2
```
> В образы уже добавлены тестовые wordlists в директорию */root/cyberscan/data*. Свои листы можно монтировать следующим образом
```sh
podman -it --rm -v /path/to/wordlist:/root/cyberscan/data/wordlists/wordlist cyberscan:0.2.2
```
