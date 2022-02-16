from selenium import webdriver
import time
import os
import yagmail

prod_url ="https://www.amazon.in/Test-Exclusive_2020_1181-Multi-3GB-Storage/dp/B089MSK447/?_encoding=UTF8&pd_rd_w=c4UQV&pf_rd_p=e932aeaf-89ea-47b8-9c31-e92696d33d85&pf_rd_r=38S2THCYBGK2952XZGJP&pd_rd_r=68d6d478-7e88-43ec-bea8-3b95eb24cd36&pd_rd_wg=UjFRp&ref_=pd_gw_ci_mcx_mr_hp_d"

sender   = "sample.00.email@gmail.com"
recevier = "bigtvindia@gmail.com" #bigtvindia@gmail.com
password = os.environ['GMAILPASS']

subject = "Alert!! PRICE DROP"

def getMailObj(sndr, passwrd):
  mailObj = yagmail.SMTP(user=sndr, password=passwrd)
  return mailObj

def sendMessage(mailObj, recvr, sub, cont):
  mailObj.send(to=recevier, subject=sub, contents=cont)
  print("EMAIL SENT!")

def getdriver(url):
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  return driver

def clean_price(price):
  price = price.replace(",","")
  return float(price.replace("₹",""))

def main():
  driver = getdriver(prod_url)
  time.sleep(1)
  element = driver.find_element(by="xpath", value='//*[@id="corePrice_desktop"]/div/table/tbody/tr[1]/td[2]/span[1]/span[2]')
  return (clean_price(element.text))


price_list =[]
price = main()
price_list.append(price)
mailObj = getMailObj(sender, password)


while True:
  time.sleep(1)
  price = main()
  price_list.append(price)
  if price_list[-1] < price_list[-2]:
    content = f'price dropped by {price_list[-2] -  price_list[-1]} \n Link : {prod_url}'
    sendMessage(mailObj, recevier, subject, content)
    pass
  del price_list[-2]
  print(price_list)
    

