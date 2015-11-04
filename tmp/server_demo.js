server = require('webserver').create();
webpage = require('webpage');

service = server.listen(9999,
  function (request, response) {
    // create and set page
    var page = webpage.create();
    page.viewportSize = {
      width: 1280,
      height: 720
    }
    page.settings = {
      javascriptEnabled: true,
      loadImages: false,
      userAgent: 'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HM NOTE 1LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025478 Mobile Safari/533.1 MicroMessenger/6.3.5.49_r55a68be.640 NetType/WIFI Language/zh_CN'
    }

    var url = request.post['url'];

    //page.onLoadFinished = function(status) {
    //  //console.log(page.content);
    //  response.write(page.content);
    //  page.close();
    //  response.close();
    //};
    page.onLoadFinished = function(status) {
      page.evaluateJavaScript(
        function() { window.scrollTo(0,100) }
      );
    }

    page.open(url, function (status) {
      console.log(status);
      response.write(page.content);
      page.close();
      response.close();
    });
    //response.write('');
    //response.close();
  }
)
