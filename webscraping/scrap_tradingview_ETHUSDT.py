#pip install selenium

from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.by import By

now = datetime.now()
str_datetime = now.strftime("%Y-%m-%d %H:%M")

interval = '1h'
symbol = 'ETHUSDT'
base_url = "https://s.tradingview.com/embed-widget/technical-analysis/?locale=es#%7B%22interval%22%3A%22"+interval+"%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Afalse%2C%22height%22%3A%22450%22%2C%22symbol%22%3A%22BINANCE%3A"+symbol+"%22%2C%22showIntervalTabs%22%3Atrue%2C%22colorTheme%22%3A%22light%22%2C%22utm_source%22%3A%22192.168.1.11%22%2C%22utm_medium%22%3A%22widget%22%2C%22utm_campaign%22%3A%22technical-analysis%22%7D"

options = Options()
options.headless = True

firefoxService = Service('/home/lbisaro/.local/lib/python3.8/site-packages/selenium/webdriver/firefox/geckodriver')
driver = webdriver.Firefox(options=options, service=firefoxService)
driver.implicitly_wait(2)
#verificationErrors = []
#accept_next_alert = True

print("\n")

driver.get(base_url)
time.sleep(4)

action = driver.find_element(By.CSS_SELECTOR,"#widget-technical-analysis-container>div>div>div>span:nth-of-type(2)");
print(action.text)


csvLine = str_datetime+';'+symbol+';'+action.text+';'+"\n"

filename = 'tradingview_'+symbol+'.csv'

try:
    f = open(filename)
except IOError:
    f = open(filename,'w')
    csvHead = 'DateTime'+';'+'Ticker'+';'+'Accion'+';'+"\n"
    f.write(csvHead)
finally:
    f.close()

f = open(filename,'a')
f.write(csvLine)
f.close()



print("\n")

driver.quit()