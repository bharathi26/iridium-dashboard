var socketct = 0;

$(document).ready(function() {
	var url = "http://" + document.domain + ":" + location.port;
    var socket = io.connect(url + "/ws");
    socket.on('msg', function(msg) {

    	if (socketct == 0){ // fixes a bug with displaying the chart 
    		LineChart.removeData();
    	} else if (socketct > 30){ // only show the last x data points
    		LineChart.removeData();
    	}

    	console.log(JSON.stringify(msg));

    	var timestamp = msg.timestamp;
    	var in_rate = msg.in_rate;
    	var in_rate_avg = msg.in_rate_avg;
		var queue_len = msg.queue_len;
		var queue_len_max = msg.queue_len_max;
		var out_rate = msg.out_rate;
		var ok_ratio = msg.ok_ratio;
		var ok_rate = msg.ok_rate;
		var ok_ratio_total = msg.ok_ratio_total;
		var ok_count_total = msg.ok_count_total;
        var out_count = msg.out_count
		var ok_rate_avg = msg.ok_rate_avg;
		var drop_count_total = msg.drop_count_total;
        var drop_count = msg.drop_count

    	LineChart.addData([in_rate, in_rate_avg, queue_len, queue_len_max, out_rate, ok_rate, ok_ratio_total], timestamp);
	    
    	$("#ok_count_total").html(ok_count_total);
    	$("#drop_count_total").html(drop_count_total);

    	$("#ok_ratio").html(ok_ratio);
        $("#ok_rate_avg").html(ok_rate_avg);

        $("#out_count").html(out_count);
        $("#drop_count").html(drop_count);


	    socketct++;
    });
});