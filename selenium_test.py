from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
   command_executor = 'http://127.0.0.1:9515',
   desired_capabilities = DesiredCapabilities.CHROME
)

driver.get("http://www.baidu.com")

print driver.page_source
f.close()
driver.close()