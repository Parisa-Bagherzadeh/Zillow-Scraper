from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import time, random

options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
# options.add_argument("--headless")




options.add_argument("--start-maximized")



def scrape():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # wait = WebDriverWait(driver, 20)
    # action = ActionChains(driver)

    # time.sleep(random.uniform(1, 3))
    # Save cookies
    # cookies = driver.get_cookies()
    # # To load cookies
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    time.sleep(1)
    # driver.get("https://www.zillow.com")
    url = "https://www.zillow.com/homes/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2222201%20Wayside%20Mission%20Viejo%2C%20CA%2092692%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.63826221227646%2C%22east%22%3A-117.63495773077011%2C%22south%22%3A33.63898317222632%2C%22north%22%3A33.64114474566528%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12773%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A18%7D"
    driver.get(url)


    # input_text = driver.find_element(By.TAG_NAME,"input")
    # input_text.clear
    # time.sleep(1)
    # driver.save_screenshot("screenshot.png")
    # time.sleep(3)
    # input_text.send_keys(zip_code)
    # input_text.submit()
    # time.sleep(3)
    # driver.save_screenshot("screenshot1.png")
    input_element = driver.find_element(By.ID,"srp-search-box")
    input_element= driver.find_element(By.TAG_NAME,"input")
    input_element.clear()
    driver.execute_script(f"var span = document.createElement('span'); span.setAttribute('data-component-name', 'tag');span.textContent ='Plano, Tx'; arguments[0].appendChild(span);", input_element)
    span = driver.find_element(By.TAG_NAME,"span")
    print(span.text)
    input_element.send_keys(zip_code)
    input_element.click()
    input_element.submit()
    input_element.send_keys(Keys.ENTER)
    text = input_element.get_attribute('value')
    print(text)
    # driver.implicitly_wait(10)
    driver.save_screenshot("screenshot9999.png")
    time.sleep(3)

                    
    div_element = driver.find_element(By.CSS_SELECTOR,"div.exposed-filters")
    buttons = div_element.find_elements(By.TAG_NAME,"button")

    # Print the text of each button
    for button in buttons:
        print(button.text)
        if button.text == "For Sale":
            button.click()
            button.send_keys(Keys.ENTER)
            if for_sale == "sale":
                driver.find_element(By.CSS_SELECTOR,"input[value^='isForSale'][type='radio']").click()
                button.submit()
                time.sleep(2)
            else:
                driver.find_element(By.XPATH,"//input[@type = 'radio'and @value ='isForRent']").click()
                # button.submit()
                time.sleep(2)
    
        if button.text == "Price":
            button.click()
            button.send_keys(Keys.ENTER)
            # button.submit()
            # driver.find_element(By.XPATH,"//button[@data-test = 'price-filters-button']").value_of_css_property = min_price
            # time.sleep(2)
            min = driver.find_element(By.XPATH, "//input[@aria-label = 'Price min']")
            min.value = min_price
            max = driver.find_element(By.XPATH, "//input[@aria-label = 'Price max']")
            max.value = max_price

        time.sleep(1)
        
        # if button.text == "Beds & Baths":
        #     button.click()
        #     bedsrooms = driver.find_element(By.XPATH,"//div[@name = 'beds-form']")
        #     bed = bedsrooms.find_elements(By.TAG_NAME,"button")

        #     for b in bed:
        #         print(b.text)
        #         if b.text == nbeds:
        #             b.click()
        #             break

        #     bathrooms = driver.find_element(By.XPATH, "//div[@name = 'baths-options']")    
        #     bathroom = bathrooms.find_elements(By.TAG_NAME,"button")

        #     for bath in bathroom:
        #         if bath.text == nbath:
        #             bath.click()
        #             break
        
        time.sleep(2)
    # btn_save = driver.find_element(By.XPATH,"//button[text()='Save search']")  
    # print(btn_save.text)
    # btn_save.click()  
    
    # mail = driver.find_element(By.XPATH,"//input[@id = 'reg-login-email']")
    # mail.value = email

    # submit = driver.find_element(By.XPATH,"//input[@type='submit']")
    # submit.click()
    # time.sleep(10)
    img_src = driver.find_elements(By.TAG_NAME,'img')
    for img in img_src:
        src = img_src.get_attribute("src")
        # src = img_src.find_element(By.)
        print(src)


    driver.quit()


if __name__ =="__main__":
    # for_sale = input("for sale/rent : ")
    # min_price = input("Min price : ")
    # max_price = input ("Max price : ")
    # beds = input("Beds : ")
    for_sale = "rent"
    min_price = "200"
    max_price = "600"
    nbeds = "2+"
    nbath = "1+"
    zip_code = 'Plano, TX'
    email = "a@gmail.com"
    scrape()
