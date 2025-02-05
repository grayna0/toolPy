from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import requests
import apiUrl 
# thư viện conver audio to text
import speech_recognition as sr
# Đường dẫn đến thư mục chứa BrowserMob Proxy
import os

from user_path import userPath, proxy_path

def downloadAudio(Url_video):
    _path = os.path.dirname(os.path.abspath("functions"))  # Lấy đường dẫn tuyệt đối đến 
    browsermob_proxy_path = proxy_path
    # Khởi động BrowserMob Proxy server
    server = Server(browsermob_proxy_path)
    server.start()
    proxy = server.create_proxy()

    # Cấu hình Selenium để sử dụng prox y
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={proxy.proxy}")
    chrome_options.add_argument("--ignore-certificate-errors") 
    chrome_options.add_argument("--ignore-ssl-errors") 
    chrome_options.add_argument("--disable-web-security")
    capabilities = DesiredCapabilities.CHROME
    capabilities['proxy'] = {
        "httpProxy": proxy.proxy,
        "sslProxy": proxy.proxy,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }

    # Khởi tạo WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Bắt đầu ghi lại lưu lượng mạng
    proxy.new_har("site_har")

    # Mở trang web mục tiêu
    url = Url_video
    driver.get(url)
    time.sleep(20)

    # Lấy dữ liệu HAR (HTTP Archive)
    har_data = proxy.har
    # Dừng proxy và server
    driver.quit()
    server.stop()

    # Lấy tất cả các URL từ HAR data
    listUrl=[]
    for entry in har_data['log']['entries']:
        request = entry['request']
        startLink = apiUrl.API_Get_audio_video
        if startLink in request['url'] and "https://data.bilibili.com/log" not in request['url']: 
            listUrl.append(request['url'])

    # Lấy đường dẫn subtitles
    # for entry in har_data['log']['entries']:
    #     request = entry['request']
    #     startLink = apiUrl.Api_sub  
    #     if startLink in request['url']: 
    #         listUrl.append(request['url'])
    # Lọc ra các URL duy nhất
    unique_VA = []
    for url in listUrl:
        if url not in unique_VA:
           unique_VA.append(url) 
    # DOWNLOAD VIDEO AND AUDIO => TÊN FILE = file_id(0,1,2,3).mp4
    for index, url in enumerate(unique_VA):
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{_path}/file_{index}.mp4','wb') as file:
                file.write(response.content)
        else:
            print("failed to download file")        
    # CONVERT audio to text format