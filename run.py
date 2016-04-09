import requests
import time
import random
import datetime

while True:
	timestamp = time.time()
	in_rate = random.randint(0,100)
	in_rate_avg = random.randint(0,100)
	queue_len = random.randint(0,100)
	queue_len_max = random.randint(0,100)
	out_rate = random.randint(0,100)
	ok_ratio = random.randint(0,100)
	ok_rate = random.randint(0,100)
	ok_ratio_total = random.randint(0,100)
	ok_count_total = random.randint(0,100)
	ok_rate_avg = random.randint(0,100)
	drop_count_total = random.randint(0,100)

	payload = {'timestamp': timestamp, 'in_rate': in_rate, 'in_rate_avg': in_rate_avg, 'queue_len': queue_len, 'queue_len_max': queue_len_max, 'out_rate': out_rate, 'ok_ratio': ok_ratio, 'ok_rate': ok_rate, 'ok_ratio_total': ok_ratio_total, 'ok_count_total': ok_count_total, 'ok_rate_avg': ok_rate_avg, 'drop_count_total': drop_count_total }

	r = requests.get('http://localhost:5000/post', params=payload)
	print r.status_code
	time.sleep(1)
	