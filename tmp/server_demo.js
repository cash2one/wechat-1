server = require('webserver').create();

service = server.listen(port, {'keepAlive': true},
  function (request, response) {
    
  }
)