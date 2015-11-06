server = require('webserver').create();
webpage = require('webpage');

service = server.listen(9999,
  function (request, response) {
    var url = request.post['url'];

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

    page.onLoadFinished = function(status) {
      page.evaluateJavaScript(
        function() {
          window.scrollTo(0,100);
        }
      );
    }

    var start_time = Date.now();
    var end_time = null;
    page.open(url, function (status) {
      end_time = Date.now();
      if ("success" === status) {
        console.log("Spend time:" + (end_time - start_time) + "ms");
        response.write(page.content);
      } else {
        response.write("error");
      };
      page.close();
      response.close();
    });



  }
)
