from gevent import monkey
monkey.patch_all()

import cgi
from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO
from flask.ext.mysql import MySQL
from flask import jsonify
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'iridium'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'iridium'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

def insertData(in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,ok_rate_avg,drop_count_total,ts):
    query = "INSERT INTO `iridium`.`iridium` (`id`, `in_rate`,`in_rate_avg`,`queue_len`,`queue_len_max`,`out_rate`,`ok_ratio`,`ok_rate`,`ok_ratio_total`,`ok_count_total`,`ok_rate_avg`,`drop_count_total`,`ts`) VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\"%s\");" % (in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,ok_rate_avg,drop_count_total,ts)
    cursor.execute(query)
    conn.commit()

def getData():
    cursor.execute("SELECT *, DATE_FORMAT(FROM_UNIXTIME(ts),'%Y-%d-%m %T') as formatted_ts FROM iridium ORDER BY id DESC LIMIT 1440")
    return cursor.fetchall()

def jsonData():
    cursor.execute("SELECT *, DATE_FORMAT(FROM_UNIXTIME(ts),'%Y-%d-%m %T') as formatted_ts FROM iridium ORDER BY id DESC LIMIT 1440")
    return jsonify(data=cursor.fetchall())

def clean(val):
    return cgi.escape(request.args.get(val, ''))

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/view')
def view():
    data = getData()
    return render_template('view.html', data=data)

@app.route('/json')
def test():
    return jsonData()

@app.route('/post')
def postdata():
    timestamp = cgi.escape(request.args.get('timestamp', ''))
    timestamp_pretty = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%m-%d %H:%M:%S')
    #timestamp_pretty = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    in_rate = clean('in_rate')
    in_rate_avg = clean('in_rate_avg')
    queue_len = clean('queue_len')
    queue_len_max = clean('queue_len_max')
    out_rate = clean('out_rate')
    ok_ratio = clean('ok_ratio')
    ok_rate = clean('ok_rate')
    ok_ratio_total = clean('ok_ratio_total')
    ok_count_total = clean('ok_count_total')
    ok_rate_avg = clean('ok_rate_avg')
    drop_count_total = clean('drop_count_total')

    insertData(in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,ok_rate_avg,drop_count_total,timestamp)

    socketio.emit('msg', {'timestamp': timestamp_pretty, 'in_rate': in_rate, 'in_rate_avg': in_rate_avg, 'queue_len': queue_len, 'queue_len_max': queue_len_max, 'out_rate': out_rate, 'ok_ratio': ok_ratio, 'ok_rate': ok_rate, 'ok_ratio_total': ok_ratio_total, 'ok_count_total': ok_count_total, 'ok_rate_avg': ok_rate_avg, 'drop_count_total': drop_count_total }, namespace='/ws')

    return 'OK';

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000, debug=True)
