# on production we would want to send static files using nginx directly, for that we will need to collect static files
# in the folder defined in the setting.py STATIC_ROOT

echo "Running migrate"
python manage.py migrate

if ["$PRODUCTION" == "true"]
then
    gunicorn givers.wsgi:application --bind 0.0.0.0:8000 --reload
else
    python manage.py runserver 0.0.0.0:8000
fi