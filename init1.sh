#sudo ln -s /home/box/web/etc/test.conf /etc/nginx/sites-enabled/default
sudo cp /home/box/web/etc/test.conf /etc/nginx/sites-enabled/default
sudo service nginx restart
