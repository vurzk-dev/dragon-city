// Manejador de errores de Dragon City
(function () {
    var server = "https:\/\/dc-canvas.socialpointgames.com\/dragoncity\/web\/",
        jsErrorUrl = "\/dragoncity\/web\/log\/error\/js",
        userId = "100001560160383",
        stackAll = [],
        permissionDenied = 'Permission denied',
        notDefined = 'is not defined';
    window.onerror = function (msg, file, line) {
        if (msg != 'Script error.' &&
            msg.match(/Location.toString/) === null &&
            msg.match(/Permission denied to access property 'toString'/) === null &&
            msg.slice(0, permissionDenied.length) != permissionDenied
        ) {
            file = (server == file.substr(0, server.length)) ? file.substr(server.length) : file;
            var params = [
                'msg='  + encodeURIComponent(msg),
                'file=' + encodeURIComponent(file),
                'line=' + encodeURIComponent(line || 0)
            ].join('&');
            if (stackAll.indexOf(params) < 0) {
                stackAll.push(params);
                params += '&user='+ encodeURIComponent(userId || '');
                params += '&_='+ encodeURIComponent(+new Date);
                if (msg == 'Error loading script' || msg.slice(- notDefined.length) == notDefined) { params += '&knowed_issue=1'; }
                try {
                    (new Image()).src = jsErrorUrl + (jsErrorUrl.indexOf('?') >= 0 ? '&' : '?') + params;
                } catch(e) {
                    console.log(['Error Tracking JS Errors', params, 'not sended'])
                }
            }
        }
    };
}());
