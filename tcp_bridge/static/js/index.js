
var $textfield;
var ws;

$(document).ready(function() {
    //Get jQuery variables
	$textfield = $('#textfield');
    //Init WebSocket
    var ws_scheme = "ws"
    var ws_path = ws_scheme + '://' + window.location.host + "/ws/text/";
    ws  = new ReconnectingWebSocket(ws_path);
    ws.onopen = function(e) {
        console.log('WebSocket is open.');
    };
    ws.onclose = function(e) {
        console.log('WebSocket is closed.');
    };
    ws.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var text = data['text'];
        $textfield.text(text);
    };
});
