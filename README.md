# Tinkoff Test Api

If you need to use this script:

1. You need to create "setting.py" file;
2. Create in "settings.py" "token" variable;
3. "token" use in "rest_wrapper.py" script for access to you tinkoff invest profile.

Token is used only in this script and don't send anywhere.


> MIGRATE NOTE
1. set FLASK_APP=manage.py
2. flask db init
3. flask db migrate
4. flask db upgrade