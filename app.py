from gevent import monkey
monkey.patch_all()

import cgi
from flask import Flask, render_template, request, jsonify
from flask.ext.socketio import SocketIO
from flask.ext.mysql import MySQL
from MySQLdb.cursors import DictCursor

import datetime
import numpy as np
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)
socketio = SocketIO(app)

mysql = MySQL(cursorclass = DictCursor)
app.config['MYSQL_DATABASE_USER'] = 'iridium'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'iridium'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def insertData(in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,out_count,ok_rate_avg,drop_count_total,drop_count,ts):
    query = "INSERT INTO `iridium`.`iridium` (`id`, `in_rate`,`in_rate_avg`,`queue_len`,`queue_len_max`,`out_rate`,`ok_ratio`,`ok_rate`,`ok_ratio_total`,`ok_count_total`,`out_count`,`ok_rate_avg`,`drop_count_total`,`drop_count`,`ts`) VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\"%s\");" % (in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,out_count,ok_rate_avg,drop_count_total,drop_count,ts)
    cursor.execute(query)
    conn.commit()

def getData():
    cursor.execute("SELECT *, DATE_FORMAT(FROM_UNIXTIME(ts),'%Y-%m-%d %T') as formatted_ts FROM iridium ORDER BY id DESC LIMIT 1440")
    return cursor.fetchall()

def getInitData():
    cursor.execute("SELECT *, DATE_FORMAT(FROM_UNIXTIME(ts),'%m-%d %T') as formatted_ts FROM iridium ORDER BY id DESC LIMIT 30")
    return cursor.fetchall()

def jsonData():
    cursor.execute("SELECT *, DATE_FORMAT(FROM_UNIXTIME(ts),'%Y-%m-%d %T') as formatted_ts FROM iridium ORDER BY id DESC LIMIT 1440")
    return jsonify(data=cursor.fetchall())

def clean(val):
    return int(round(float(cgi.escape(request.args.get(val, '')))))

@socketio.on('connect', namespace='/ws')
def wsconnect():
    data = getInitData()
    for item in reversed(data):
        socketio.emit('msg', {'timestamp': item['formatted_ts'], 'in_rate': item['in_rate'], 'in_rate_avg': item['in_rate_avg'], 'queue_len': item['queue_len'], 'queue_len_max': item['queue_len_max'], 'out_rate': item['out_rate'], 'ok_ratio': item['ok_ratio'], 'ok_rate': item['ok_rate'], 'ok_ratio_total': item['ok_ratio_total'], 'ok_count_total': item['ok_count_total'],  'out_count': item['out_count'],'ok_rate_avg': item['ok_rate_avg'], 'drop_count_total': item['drop_count_total'], 'drop_count': item['drop_count']}, namespace='/ws')

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

@app.route('/bokeh')
def run():
    data = getData()
    dates = []
    in_rate = []
    in_rate_avg = []
    queue_len = []
    queue_len_max = []
    out_rate = []
    ok_ratio =[]
    ok_ratio_total = []
    ok_count_total = []
    out_count = []
    ok_rate_avg = []
    drop_count_total = []
    drop_count = []

    for item in data:
        #print item["id"], item["formatted_ts"], item["in_rate"]
        dates.append(pd.to_datetime(item["formatted_ts"]))
        in_rate.append(item["in_rate"])
        in_rate_avg.append(item["in_rate_avg"])
        queue_len.append(item["queue_len"])
        queue_len_max.append(item["queue_len_max"])
        out_rate.append(item["out_rate"])
        ok_ratio.append(item["ok_ratio"])
        ok_ratio_total.append(item["ok_ratio_total"])
        ok_count_total.append(item["ok_count_total"])
        out_count.append(item["out_count"])
        ok_rate_avg.append(item["ok_rate_avg"])
        drop_count_total.append(item["drop_count_total"])
        drop_count.append(item["drop_count"])

    np_dates = np.array(dates, dtype='M8[m]')
    np_in_rate = np.array(in_rate)
    np_in_rate_avg = np.array(in_rate_avg)
    np_queue_len = np.array(queue_len)
    np_queue_len_max = np.array(queue_len_max)
    np_out_rate = np.array(out_rate)
    np_ok_ratio = np.array(ok_ratio)
    np_ok_ratio_total = np.array(ok_ratio_total)
    np_ok_count_total = np.array(ok_count_total)
    np_out_count = np.array(out_count)
    np_ok_rate_avg = np.array(ok_rate_avg)
    np_drop_count_total = np.array(drop_count_total)
    np_drop_count = np.array(drop_count)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
   
    p = figure(width=1600, height=600, x_axis_type="datetime")
    p1 = figure(width=1600, height=600, x_axis_type="datetime")

    # add renderers
    p.line(np_dates, np_in_rate, color='#f0341f', legend='in_rate')
    p.line(np_dates, np_in_rate_avg, color='navy', legend='in_rate_avg')
    p.line(np_dates, np_queue_len, color='#636154', legend='queue_len')
    p.line(np_dates, np_queue_len_max, color='#6ac6f9', legend='queue_len_max')
    p.line(np_dates, np_out_rate, color='#000000', legend='out_rate')
    p.line(np_dates, np_ok_ratio, color='#ffb748', legend='ok_ratio')
    p.line(np_dates, np_ok_ratio_total, color='#CAB2D6', legend='ok_ratio_total')
    p.line(np_dates, np_out_count, color="red", legend="out_count")
    p.line(np_dates, np_ok_rate_avg, color='#ff65ff', legend='ok_rate_avg')
    p.line(np_dates, np_drop_count_total, color='#564269', legend='drop_count_total')
    p.line(np_dates, np_drop_count, color="blue", legend="drop_count")

    p1.line(np_dates, np_ok_count_total, color='#174517', legend='ok_count_total')

    # NEW: customize by setting attributes
    p.title = "Iridium"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha=0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Rate'
    p.ygrid.band_fill_color="white"
    p.ygrid.band_fill_alpha = 0.1

    p1.title = "Iridium"
    p1.legend.location = "top_left"
    p1.grid.grid_line_alpha=0
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Rate'
    p1.ygrid.band_fill_color="white"
    p1.ygrid.band_fill_alpha = 0.1

    plots = {'main': p, 'total': p1}
    script, div = components(plots)

    return render_template('bokeh.html', script=script, div=div)


@app.route('/post')
def postdata():
    timestamp = cgi.escape(request.args.get('timestamp', ''))
    timestamp_pretty = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%m-%d %H:%M:%S')
   
    in_rate = clean('in_rate')
    in_rate_avg = clean('in_rate_avg')
    queue_len = clean('queue_len')
    queue_len_max = clean('queue_len_max')
    out_rate = clean('out_rate')
    ok_ratio = clean('ok_ratio')
    ok_rate = clean('ok_rate')
    ok_ratio_total = clean('ok_ratio_total')
    ok_count_total = clean('ok_count_total')
    out_count = clean('out_count')
    ok_rate_avg = clean('ok_rate_avg')
    drop_count_total = clean('drop_count_total')
    drop_count = clean('drop_count')

    insertData(in_rate,in_rate_avg,queue_len,queue_len_max,out_rate,ok_ratio,ok_rate,ok_ratio_total,ok_count_total,out_count,ok_rate_avg,drop_count_total,drop_count,timestamp)

    socketio.emit('msg', {'timestamp': timestamp_pretty, 'in_rate': in_rate, 'in_rate_avg': in_rate_avg, 'queue_len': queue_len, 'queue_len_max': queue_len_max, 'out_rate': out_rate, 'ok_ratio': ok_ratio, 'ok_rate': ok_rate, 'ok_ratio_total': ok_ratio_total, 'ok_count_total': ok_count_total, 'out_count': out_count, 'ok_rate_avg': ok_rate_avg, 'drop_count_total': drop_count_total, 'drop_count': drop_count }, namespace='/ws')

    return 'OK';

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000, debug=True)
