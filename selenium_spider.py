from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()

driver.get("http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA4ODQ3MjY4MQ==&uin=MTIzOTkyMDUzOQ%3D%3D&key=41ecb04b05111003345d8fc7d7d8c39c83315cf8403b7acc4ce5c0f102e0e77e4e51d36f1d958be8073697d45c63ffcd&devicetype=android-19&version=26030849&lang=zh_CN&nettype=WIFI&pass_ticket=UTTrhEGgJukIpA6VoibWbq1t7FrjhpKFkGyNmVCFd0yjBD6ic2oKw1%2FAoRwvSlbT")

print driver.page_source
driver.close()
