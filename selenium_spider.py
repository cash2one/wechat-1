from selenium import webdriver

driver = webdriver.Firefox()

driver.get("http://www.baidu.com")

print driver.page_source
f.close()
driver.close()