#sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
#sudo gunicorn -c /etc/gunicorn.d/hello.py hello:hello_app -D
sudo ln -sf /home/box/web/etc/django.py /etc/gunicorn.d/django.py
sudo gunicorn -c /etc/gunicorn.d/django.py ask.wsgi:application -D
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo service nginx restart

sudo /etc/init.d/mysql start
#sudo systemctl start mariadb
#mysql -uroot -e "DROP DATABASE IF EXISTS askappdb;"
#mysql -uroot -e "DROP USER 'askapp'@'localhost';" mysql
mysql -uroot -e "CREATE DATABASE askappdb;"
mysql -uroot -e "CREATE USER 'askapp'@'localhost' IDENTIFIED BY 'passwrd123';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON askappdb.* TO 'askapp'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"

sudo python ~/web/ask/manage.py makemigrations qa
sudo python ~/web/ask/manage.py migrate
