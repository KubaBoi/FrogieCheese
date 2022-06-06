# postgres

```python
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ 'lsb_release -cs'-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
apt show postgresql
sudo -u postgres psql
psql
alter user postgres PASSWORD 'admin';
ALTER ROLE
CREATE DATABASE frogie_database;
\q
sudo -u postgres psql frogie_database
copy paste setDatabase.sql
```

# build

```
 - v pom musi byt <packaging>war<packaging>
pred buildem je potreba pridat do hlavni tridy:
    import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
    extends SpringBootServletInitializer
a do pom:
        <dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-tomcat</artifactId>
			<scope>provided</scope>
		</dependency>

apt install maven
mvn clean
mvn package

/manager/html
	- /
	- <version> from pom
	- nic
	- /home/Frogie/target/<version>.war
```

# tomcat (https://linuxhint.com/install_apache_tomcat_server_ubuntu/)

```
sudo apt-cache search tomcat
sudo apt install tomcat9 tomcat9-admin
ss -ltn
sudo ufw allow from any to any port 8080 proto tcp
sudo nano /etc/tomcat9/tomcat-users.xml
	<role rolename="manager-gui"/>
	<user username="tomcat" password="admin" roles="manager-gui"/>

sudo systemctl restart tomcat9
<ip>:8080/manager/html
Deploy menu - XML Configuration file path zustane prazdne
sudo nano /etc/rc.local:
	#!/bin/bash
	sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

sudo chmod a+x /etc/rc.local
```

# cloud

```
ssh root@94.176.182.223
sudo apt install libpq-dev python3-dev
pip install psycopg2-binary
pip install psycopg2
sudo crontab -e
@reboot python3 /home/Cloudos/server.py &
sudo ufw allow from any to any port 8000 proto tcp
```
