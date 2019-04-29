sudo /etc/init.d/mysql start
#sudo systemctl start mariadb
#mysql -uroot -e "DROP DATABASE IF EXISTS askappdb;"
#mysql -uroot -e "DROP USER 'askapp'@'localhost';" mysql
mysql -uroot -e "CREATE DATABASE askappdb;"
mysql -uroot -e "CREATE USER 'askapp'@'localhost' IDENTIFIED BY 'passwrd123';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON askappdb.* TO 'askapp'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"