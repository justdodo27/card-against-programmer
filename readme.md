## First run:

1. Create vue files
    - ``cd vueapp``
    - ``npm run serve`` or ``yarn serve``
    - close vueapp
2. Collect staticfiles
    - ``python3 manage.py collectstatic``
3. Create database
    - ``python3 manage.py makemigrations``
    - ``python3 manage.py migrate``
    - ``python3 manage.py createsuperuser``
4. Run server
    - ``python3 manage.py runserver``