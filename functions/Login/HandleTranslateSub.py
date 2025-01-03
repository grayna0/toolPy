
import sys
sys.path.insert(0, "C:/Users/pc/myPyPro/functions")
import apiUrl as url
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import Get_Sub_bilibili
import psutil
def HandleTranslateSub():
    listSub= Get_Sub_bilibili.getSub(api_url="https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/11366157831821727370983317570cffb8cc19ee6136fffb6001a9e610?auth_key=1735897413-73ef08ccd7684c0e9b36064f3455d633-0-5cd1b7de0e65ee6b9ead5ba72cdd67d1",video_id="https://www.bilibili.com/video/BV1ZKBKY2ESC/?spm_id_from=333.337.search-card.all.click&vd_source=1124f7b904b73e398c740b637205feb4")
    end_point_slice= len(listSub)//20
    star_point_slice = 0    
    # Kill existing Chrome processes
    os.system("taskkill /f /im chrome.exe 2>nul")
    def kill_chrome_processes():
        for proc in psutil.process_iter():
            try:
                if proc.name() == "chrome.exe":
                    proc.kill()
            except:
                pass
        time.sleep(2)

    # Chrome configuration
    CHROME_PATH = os.path.expandvars("%LOCALAPPDATA%/Google/Chrome/User Data")
    DEBUGGING_PORT = 9222
    # Setup Chrome options
    options = uc.ChromeOptions()
    options.add_argument('--profile-directory=Default')
    options.add_argument(f'--remote-debugging-port={DEBUGGING_PORT}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # wait render text 
    def wait_for_complete_response(driver, timeout=30,i=0):
        i=2 if i == 0 else i*2
        
        try:
            # Wait for loading indicator to disappear
            # wait = WebDriverWait(driver, timeout)
            
            # Get response element
            response_element = wait.until(EC.presence_of_element_located((
                By.XPATH, f"/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[{i}]/div/div/div[2]/div/div[1]/div/div/div"
            )))
            wait.until(EC.presence_of_element_located((
                By.XPATH,"//div[contains(@class, 'markdown')]"
            )))
            
            # Wait for text content to stabilize
            last_text = ""
            current_text = response_element.text
            
            while last_text != current_text:
                time.sleep(1)
                last_text = current_text
                current_text = response_element.text
                
            return current_text        
        except Exception as e:
            print(f"Error waiting for response: {str(e)}")
            return None
    # Create Chrome session
    def create_driver(max_attempts=3):
            for attempt in range(max_attempts):
                try:
                    driver = uc.Chrome(options=options)
                    return driver
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(2)
            raise Exception("Failed to create Chrome session after multiple attempts")

        # send and get text response from chatgpt
    result_ask=""
    driver = uc.Chrome(options=options,user_data_dir=CHROME_PATH,)  
    for i in range(21):
        # driver = create_driver()
        print(i)
        if i == 0:
            driver.get(url.chatgpt__url)
        try:
            wait = WebDriverWait(driver, 10)
            textarea = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//*[@id='prompt-textarea']"
                )))
            textarea.click()
            time.sleep(2)
            textarea.send_keys(f"{listSub[star_point_slice : end_point_slice ]} dịch sang tiếng việt ")
            time.sleep(10)
            
            textarea = wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='composer-background']/div[2]/button"
            )))
            textarea.click()
            time.sleep(20)
            text_Rp = wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[1]/div/div/div"
            )))
            index__rp = i 
            text_respond=wait_for_complete_response(driver,i=index__rp)
            
            # write the response to a Array
            result_ask+=text_respond
            star_point_slice= end_point_slice
            end_point_slice += len(listSub)//20
            # driver.quit()
            time.sleep(10)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            time.sleep(5)
            
    with open("C:/Users/pc/myPyPro/result/vietSub.txt", "a+",encoding="utf-8") as file:
        file.write(result_ask)
HandleTranslateSub()