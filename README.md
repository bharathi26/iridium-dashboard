# iridium-dashboard
Browser based dashboard for the [gr-iridium](https://github.com/muccc/gr-iridium) and [iridium-toolkit](https://github.com/muccc/iridium-toolkit) built with Flask, Websockets, Bootstrap, MySQL, Bokeh and Charts.js

![iridium-dashboard](https://raw.githubusercontent.com/devnulling/iridium-dashboard/master/images/dashboard.png)

### Requisites

 * Python (2.7)
 * Flask
 * Flask-SocketIO
 * Flask-MySQL
 * Gevent 
 * MySQL
 * Bokeh
 * Pandas
 * Requests
 * NumPY


#### Install MySQL

    sudo apt-get install mysql-server mysql-client libmysqlclient-dev
    sudo mysql_install_db
    sudo mysql_secure_installation

#### Install Requisites

    sudo pip install flask flask-socketio flask-mysql flask-mysqldb gevent bokeh pandas numpy requests

#### Login & Create MySQL Database

    mysql -uroot -p 
    create database iridium;

#### Create MySQL User

    CREATE USER 'iridium'@'%' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON iridium.* TO 'iridium'@'%';
    FLUSH PRIVILEGES;

#### Create Iridium Table

    mysql -u<user> -p iridium < iridium.sql

#### Edit 
Edit app.py with password set for mysql iridium user

#### Start
Start the dashboard by running 

    python app.py

Enable the dashboard from iridium-extractor with the --dashboard flag, set host or port with --port or --host flags (default is localhost:5000)

    iridium-extractor -D 4 --dashboard examples/hackrf.conf | grep "A:OK" > output.bits
