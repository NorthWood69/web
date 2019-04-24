sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo gunicorn -c /etc/gunicorn.d/hello.py hello:hello_app -D
sudo ln -sf /home/box/web/etc/django.py /etc/gunicorn.d/django.py
sudo gunicorn -c /etc/gunicorn.d/django.py ask.wsgi:application -D
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo service nginx restart