# API сервис для расчета цены перевозки

## Возможности/Features:

* Загрузка тарифа POST запросом на эндпоинт http://localhost:8080/tariffs/.
Тариф загружается в формате json. 
* Расчет стоимости доставки по дате и коэффициенту от стоимости груза. 
Стоимость груза задается пользователем. 
Эндпоинт http://localhost:8080/calculate_insurance_cost/.

## Установка/Installation
* Docker и docker-compose должны быть установлены. Если нет, то сделайте это по 
инструкции:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru
* Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/Yohimbe227/Cargo.git
```
* Перейдите в папку infra внутри папки /Cargo.
* Переименуйте файл .env.example в .env
* А теперь просто запустите:
```bash
docker-compose up
```
## Author
 Юрий Каманин 
 [@Yohimbe227](https://www.github.com/Yohimbe227)
