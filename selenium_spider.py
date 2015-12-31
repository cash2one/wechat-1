from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(720, 1280))
display.start()
driver = webdriver.Chrome()

driver.get("http://www.baidu.com")

f = open("baidu.html", "w")
f.write(driver.page_source)
f.close()
driver.close()
