# Установка
**1.** git clone [https://github.com/vkorzhovv/leasing-bot.git](https://github.com/vkorzhovv/leasing-bot.git) <br>
**2.** переходим в склонированную папку в консоли и выполняем команду: python -m venv venv. Потом активируем виртуальное окружение<br>
**3.** устанавливаем зависимости в виртуальное окружение: pip install -r requirements.txt <br>
**4.** создаём суперюзера: python manage.py createsuperuser <br>
**5.** Создаём файл .env, шаблон такого файла можно найти, перейдя в .env_template, где всё, что нужно – это заполнить пустые строки переменных своими значениями <br>
**6.** запускаем сервер django, находясь папке leasing_bot: python manage.py runserver <br>
**7.** открываем вторую консоль, переходим в leasing_bot/bot и запускаем бота: python main.py <br>
**8.** смотрим проект

# Для работы каталога 
Нужна одна корневая категория с именем "Каталог", от которой уже будут наследоваться следующие

**Для последующей работы с админ-панелью нужно создать админа через /start. Т.е. createsuperuser нужен только для того, что описывалось выше и для того, чтобы дать статус superuser реальному админу, который будет зарегистрирован через /start (это нужно, потому что джанговский superuser никак не связан с телеграмом, а это необходимо)**