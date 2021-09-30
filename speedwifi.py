import requests
from selene.browsers import BrowserName
from selene.api import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import json

# Webページを取得して解析する
load_url = "http://speedwifi-next.home/html/login.htm"
html = requests.get(load_url)
s = str(html.content)
def get_status(browser):
    ret = str(browser.execute_script("return G_MonitoringStatus;"))
    ret = ret.replace('\'', '\"')
    return ret
def main():
    try:
        config.browser_name = BrowserName.CHROME
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_option)
        browser.set_driver(driver)
        browser.open_url(load_url)
        status = get_status(browser)
        json_dict = json.loads(status)
        test = json_dict
        battery_level = json_dict['response']['BatteryLevel']
        if(int(battery_level) == 0):
            try:
                requests.get("http://localhost:8091/google-home-notifier?text=http%3A%2F%2F192.168.100.105%2Fmobile_wifi.mp3", timeout=(0.5, 2.0))
            except requests.exceptions.RequestException as e:
                print(e.__doc__.strip())
        browser.quit()
    except:
        print(traceback.format_exc())
        browser.quit()

if __name__ == '__main__':
    main()
