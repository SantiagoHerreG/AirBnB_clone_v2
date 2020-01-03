#!/usr/bin/env bash
# Configures and sets up web servers for the deployment of web_static

if [ ! -x /usr/sbin/nginx ]; then
	apt-get update
	apt-get -y install nginx
	service nginx start
fi
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Hello World" >> /data/web_static/releases/test/index.html

if [ ! -h /data/web_static/current ]; then
	ln -s /data/web_static/releases/test/ /data/web_static/current
else
	unlink /data/web_static/current
	ln -s /data/web_static/releases/test/ /data/web_static/current
fi

chown -R ubuntu:ubuntu /data/
new="\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n}"
sed -i "s@^}@$new@" /etc/nginx/sites-available/default
service nginx restart
