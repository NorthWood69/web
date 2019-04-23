sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo gunicorn -c /etc/gunicorn.d/hello.py hello:hello_app -D
sudo ln -sf /home/box/web/etc/test.conf /etc/nginx/sites-enabled/default
#sudo cp /home/box/web/etc/test.conf /etc/nginx/sites-enabled/default
sudo service nginx restart