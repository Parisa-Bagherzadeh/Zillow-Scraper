import os
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService


cur_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cur_path)
sys.path.insert(0, os.path.join(cur_path, '..'))
sys.path.insert(0, os.path.join(cur_path, '../..'))
sys.path.insert(0, os.path.join(cur_path, '../../../..'))

import functools
import json
import multiprocessing.pool
import time

from bs4 import BeautifulSoup as Soup
from easydict import EasyDict as edict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Function for timeout handling
def timeout(max_timeout):
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            try:
                return async_result.get(max_timeout)
            except Exception as e:
                print(e)
                return False

        return func_wrapper

    return timeout_decorator


class SeleniumWrapper():
    """A wrapper for selenium webdriver to make it easy to use."""

    def __init__(self, args: edict, timeout: int = 1, pdf_available: bool = False, pdf_args: edict = None):
        

        # sourcery skip: raise-specific-error
        self.args = args
        if args.device == "chrome":
            
            self.driver = webdriver.Chrome(args.driver_path)
        elif args.device == "firefox":
            self.driver = webdriver.Firefox(args.driver_path)
        elif args.device == 'server':
            options = webdriver.ChromeOptions()

          

            options.page_load_strategy = 'normal'
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument("--start-maximized")
            options.add_argument("--headless=new")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--disable-gpu')
            options.add_argument("--start-maximized")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--allow-running-insecure-content')
            
            
            if pdf_available and pdf_args is not None:
                pdf_settings = {
                    "recentDestinations": [{
                        "id": "Save as PDF",
                        "origin": "local",
                        "account": ""
                    }],
                    "selectedDestinationId": "Save as PDF",
                    "version": 2,
                    "isLandscapeEnabled": True,
                    "isHeaderFooterEnabled": False,
                    "isCssBackgroundEnabled": pdf_args.css_enabled,
                }

                options.add_argument('--enable-print-browser')
                prefs = {
                    'printing.print_preview_sticky_settings.appState': json.dumps(pdf_settings),
                    'savefile.default_directory': pdf_args.save_dir,
                }
                options.add_argument('--kiosk-printing')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument("--test-type")
                # options.add_argument("--headless=new")
                options.add_argument("--headless=new")
                options.addArguments("test-type")
                options.addArguments("start-maximized")
                # options.addArguments("--window-size=1920,1080")
                options.add_argument("--start-maximized")
                options.addArguments("--enable-precise-memory-info")
                options.addArguments("--disable-popup-blocking")
                options.addArguments("--disable-default-apps")
                options.add_argument('--ignore-certificate-errors')
                options.addArguments("test-type=browser")
                options.AddArgument("--incognito")
                options.AddArgument("--headless")
                # options.AddArgument("headless")
                options.AddArgument("--no-sandbox")
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-infobars')
                options.add_argument('--allow-running-insecure-content')
                options.add_argument('--disable-gpu')
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-dev-shm-usage")
                options.add_experimental_option('prefs', prefs)
                options.add_experimental_option('excludeSwitches', ['enable-logging'])

            self.driver = webdriver.Remote(
                command_executor=f'http://{self.args.ip}:{self.args.port}',
                options=options,
                desired_capabilities=webdriver.DesiredCapabilities.CHROME
            )
        else:
            raise Exception("Device and driver path not specified")

        self.timeout = timeout

    # close session and quit driver and distroy everything
    def close(self):
        self.driver.close()
        self.driver.quit()

    def get(self, url: str):
        self.driver.get(url)

    @timeout(10.0)
    def get_page_with_tiemout(self, url: str):
        return self.driver.get(url)


    def get_page_with_bs4(self, url: str, loc, verbose: bool = True):
        element = None
        page = None

        if verbose: print("Loading WebPage: ", url)
        time.sleep(5)
        self.get(url)
  
    
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(self.set_location(loc))
            )
       
            page =Soup(self.driver.page_source, features='html.parser')
            if verbose: print("Sending Soup: ")
        except Exception as e:
            if verbose: print("Error: In loading WebPage", e)

   
        del element
        return page

    def get_page_witout_loc(self, url: str, verbose: bool = False, timeout: int = 10):
        html = None
        page = None

        if verbose: print("Loading WebPage: ", url)

        self.get_page_with_tiemout(url)

        try:
            # Load page Completely
            html = self.driver.page_source
            page = Soup(self.driver.page_source, features='html.parser')
            if verbose: print("Sending Soup: ")
        except Exception as e:
            if verbose: print("Error: In loading WebPage", e)

        return {"page": page, "html": html}

    def get_page_content_with_bs4(self, loc, verbose: bool = False):
        element = None
        page = None
        time.sleep(5)
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.set_location(loc))
            )
            page = Soup(self.driver.page_source, features='html.parser')
            if verbose: print("Sending Soup: ")
        except Exception as e:
            if verbose: print("Error: In loading WebPage", e)

        # self.driver.close()
        del element
        return page

    # @timeout(10.0)
    def print_page_execute_script(self):
        self.driver.execute_script('window.print();')

    def save_page_pdf(self, url: str, verbose: bool = False):

        try:
            if verbose: print("Loading WebPage: ", url)
            self.driver.set_page_load_timeout(10);
            self.get_page_with_tiemout(url)
        except Exception as e:
            if verbose: print("Error: In Loading WebPage", e)
            response = False

        try:
            if verbose: print("Saving PDF: ")
            self.print_page_execute_script()
            response = True
        except Exception as e:
            if verbose: print("Error: In Saving WebPage", e)
            response = False

        self.driver.close()

        return response

    def set_location(self, loc):
        if loc[0] == "id":
            return (By.ID, loc[1])
        elif loc[0] == "name":
            return (By.NAME, loc[1])
        elif loc[0] == "xpath":
            return (By.XPATH, loc[1])
        elif loc[0] == "link_text":
            return (By.LINK_TEXT, loc[1])
        elif loc[0] == "partial_link_text":
            return (By.PARTIAL_LINK_TEXT, loc[1])
        elif loc[0] == "tag_name":
            return (By.TAG_NAME, loc[1])
        elif loc[0] == "class_name":
            return (By.CLASS_NAME, loc[1])
        elif loc[0] == "css_selector":
            return (By.CSS_SELECTOR, loc[1])
        else:
            return (By.XPATH, loc[1])

    def find_element(self, *loc):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(loc))

    def find_elements(self, *loc):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(loc))

    def find_element_by_id(self, id_):
        return self.find_element(By.ID, id_)

    def find_elements_by_id(self, id_):
        return self.find_elements(By.ID, id_)

    def find_element_by_name(self, name):
        return self.find_element(By.NAME, name)

    def find_elements_by_name(self, name):
        return self.find_elements(By.NAME, name)

    def find_element_by_xpath(self, xpath):
        return self.find_element(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(By.XPATH, xpath)

    def find_element_by_link_text(self, link_text):
        return self.find_element(By.LINK_TEXT, link_text)

    def find_elements_by_link_text(self, link_text):
        return self.find_elements(By.LINK_TEXT, link_text)

    def find_element_by_partial_link_text(self, link_text):
        return self.find_element(By.PARTIAL_LINK_TEXT, link_text)

    def find_elements_by_partial_link_text(self, link_text):
        return self.find_elements(By.PARTIAL_LINK_TEXT, link_text)

    def find_element_by_tag_name(self, name):
        return self.find_element(By.TAG_NAME, name)

    def find_elements_by_tag_name(self, name):
        return self.find_elements(By.TAG_NAME, name)

    def find_element_by_class_name(self, name):
        return self.find_element(By.CLASS_NAME, name)

    def find_elements_by_class_name(self, name):
        return self.find_elements(By.CLASS_NAME, name)

    def find_element_by_css_selector(self, css_selector):
        return self.find_element(By.CSS_SELECTOR, css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self.find_elements(By.CSS_SELECTOR, css_selector)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def __getattr__(self, name):
        return getattr(self.driver, name, None)

    def costum_function(self, xpath):
        time.sleep(5)



    def main(self,url):
          obj.get(url)
          obj.get_page_with_bs4(url, ("id","wrapper"), True) 

          input_element = obj.find_elements_by_id("srp-search-box")
        #   time.sleep(3)
          btn = input_element[0].find_element(By.TAG_NAME,"button")
          btn.click()
          input_text = input_element[0].find_element(By.TAG_NAME,"input")
          input_text.clear()
          input_text.send_keys(zip_code)
          input_text.submit()
          input_text.send_keys(Keys.ENTER)

        #   time.sleep(2)  
          btn_element = obj.find_element_by_css_selector("div.filter-buttons")
          buttons = btn_element.find_elements(By.TAG_NAME, "button")

          for button in buttons:
            print(button.text)
            if button.text == "For Sale":
                button.click()
                if for_sale == "sale":
                    obj.find_element(By.CSS_SELECTOR,"input[value^='isForSale'][type='radio']").click()
                    obj.find_element(By.CSS_SELECTOR,"input[value^='isForSale'][type='radio']").submit()
                    
                else:
                    obj.find_element(By.XPATH,"//input[@type = 'radio'and @value ='isForRent']").click()
                    obj.find_element(By.XPATH,"//input[@type = 'radio'and @value ='isForRent']").submit()
           
            break



          time.sleep(1)  
          new_url = obj.current_url
          selenium_config = edict(
          device = "server",
          ip="0.0.0.0",
          port = 1423,)
          obj1 = SeleniumWrapper(args=selenium_config)
          obj1.get(new_url)
          obj1.get_page_with_bs4(new_url, ("id","__next"), True) 

        
        
          ###############################################################
        #  Get images  
        
          list_of_imgs: Soup = obj1.get_page_content_with_bs4(("id", "grid-search-results"))
          list_of_link_imgs = list_of_imgs.find(class_="search-list-relaxed-results").findChildren("li")

          info_dict = {}

          for img in list_of_link_imgs:
              if img.find("a"):
                  image = img.find("a").get("href")
                  print(image)
                  info_dict['img'] = image
              if img.find("ul"):
                  info = img.find("ul").find("li")
                  title = img.find("span")
                  add = img.find("address")
              
                  info_dict.update({"info":info.text})
                  info_dict.update({"addresss":add.text})
                  info_dict.update({"title": title.text})

          return(info_dict)  
      
     

              
          ##################################################################    



if __name__ == '__main__':
    
    url = "https://www.zillow.com/homes/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2222201%20Wayside%20Mission%20Viejo%2C%20CA%2092692%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.63826221227646%2C%22east%22%3A-117.63495773077011%2C%22south%22%3A33.63898317222632%2C%22north%22%3A33.64114474566528%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12773%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A18%7D"
    path = '/home/parisa/web_scraping/'
    selenium_config = edict(
        device = "server",
        ip="0.0.0.0",
        port = 1423,
    )


    zip_code = "Deerfield Plano, TX"
    for_sale = "rent"
    min_price = "200"
    max_price = "2000"
    nbeds = "1+"
    nbath = "1+"
    email = "a@gmail.com"

    # Start timer
    Start = time.time()
    obj = SeleniumWrapper(args=selenium_config)   
    info = obj.main(url)

    obj.close()
    del selenium_config
    del obj
    

