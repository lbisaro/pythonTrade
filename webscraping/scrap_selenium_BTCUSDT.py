#pip install selenium

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.by import By

now = datetime.now()
str_datetime = now.strftime("%Y-%m-%d %H:%M")

ticker = 'BTCUSDT'
base_url = "https://investing.com/crypto/bitcoin/btc-usd-technical"

options = Options()
options.headless = True

firefoxService = Service('/home/lbisaro/.local/lib/python3.8/site-packages/selenium/webdriver/firefox/geckodriver')
driver = webdriver.Firefox(options=options, service=firefoxService)
driver.implicitly_wait(2)
#verificationErrors = []
#accept_next_alert = True

driver.get(base_url)
print(driver.title)

summary = driver.find_element(By.CSS_SELECTOR,".summary span");
accion = summary.text


price = driver.find_element(By.ID,"last_last")
price = price.text.replace(',', '')

print(ticker)
print(price)
print(summary.text)

tds = driver.find_elements(By.CSS_SELECTOR,"#techinalContent table.crossRatesTbl tbody tr td")

s3 = tds[1].text
s2 = tds[2].text
s1 = tds[3].text
pp = tds[4].text
r1 = tds[5].text
r2 = tds[6].text
r3 = tds[7].text


csvLine = str_datetime+';'+ticker+';'+accion+';'+price+';'+s3+';'+s2+';'+s1+';'+pp+';'+r1+';'+r2+';'+r3+';'+"\n"

filename = 'investing_'+ticker+'.csv'

try:
    f = open(filename)
except IOError:
    f = open(filename,'w')
    csvHead = 'DateTime'+';'+'Ticker'+';'+'Accion'+';'+'Price'+';'+'S3'+';'+'S2'+';'+'S1'+';'+'Pivot point'+';'+'R1'+';'+'R2'+';'+'R3'+';'+"\n"
    f.write(csvHead)
finally:
    f.close()

f = open(filename,'a')
f.write(csvLine)
f.close()

driver.quit()
