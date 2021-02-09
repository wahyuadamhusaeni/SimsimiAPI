import os

from selenium import webdriver
from selenium.webdriver import Chrome

from .log import Log
import time
import sys



class SimsimiAPI:
    def __init__(self):

        self.driver_path = self._configParser()[1]
        self.browser_mode = self._configParser()[0]
        self.browser_binary_location = self._configParser()[2]
        self.password_default = 'Admin123!@#'
        self.temp_mail_url = "https://generator.email"

        self.log = Log()
        self.driver = Chrome(options=self._get_opts(), executable_path=self.driver_path)

    def generate_email(self):

        self.log.write_log("browser", f"Browser Open")
        self.driver.get(self.temp_mail_url)

        mail_handle = self.driver.current_window_handle
        
        domain_radio = self.__get_xpath_elem("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/label").click()
        name = str( self.__get_xpath_elem('//*[@id="userName"]').get_attribute("value"))
        domain = str( self.__get_xpath_elem('//*[@id="domainName2"]').get_attribute("value"))

        mail = name + "@" + domain

        self._random_wait(1, 2)
        self.driver.execute_script('window.open("https://workshop.simsimi.com/en/login", "_blank");')
        
        simsimi_handle = self.driver.window_handles[1]
        self.driver.switch_to.window(simsimi_handle)
        self._random_wait(2, 4)

        self._click('/html/body/div/div/div[2]/div/div/form/div[3]/div[2]', "CLick Label Register")

        self.__get_xpath_elem('/html/body/div/div/div[2]/div/div/form/input[1]').send_keys(mail)
        self.__get_xpath_elem('/html/body/div/div/div[2]/div/div/form/input[2]').send_keys(self.password_default)
        self._click('/html/body/div/div/div[2]/div/div/form/button', 'Click Button Register')
        self._random_wait(4, 5)

        self._modal_register_handler()

        if self.driver.current_window_handle != mail_handle:
            self.driver.switch_to.window(mail_handle)

        code = None
        count_pass = 0
        self.log.write_log("bot", 'Waiting Verification Email')
        for count_pass in range(20):
            try:

                code = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div[2]/div[4]/div[3]/p[3]").text
                
                count_pass = 20

            except:
                time.sleep(1)
                count_pass += 1
                self.driver.refresh()

        if count_pass == 20:
            self.driver.execute_script('window.open("'+ code +'", "_blank");')
            self.sleep(5)
            self.log.write_log("bot", 'Verification Email Success')
            self.driver.switch_to.window(simsimi_handle)
            self._modal_register_handler()
            self._click('/html/body/div/div/div[2]/div/div/form/button', 'Click Button Login')
            self.sleep(5)
            self.driver.get('https://workshop.simsimi.com/dashboard?pi=0')
            self._click('/html/body/div[1]/div/div[2]/div/div[1]/div/div[2]/label', 'Active Service')
            self.sleep(5)
            api_key = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div").text
            out_file = open("akun.txt","a")
            out_file.write(mail+"|"+ self.password_default +"|" + api_key +"\n")
            out_file.close()
            self.log.write_log("success", self.log.green_text(f"{mail}|{self.password_default}|{api_key}"))
            self.quit()
            self.sleep(10)
        else:
            self.quit()
            

        



    def _modal_register_handler(self):

        try:
            self._click('/html/body/div/div/div[4]/div/button', "Close Modal")
        except Exception as e:
            pass


    def _get_opts(self):

        opts = webdriver.chrome.options.Options()

        if self.browser_mode == "headless":
            opts.add_argument("--headless")

        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.binary_location = self.browser_binary_location
        opts.add_argument("--ignore-certificate-erors")
        opts.add_argument("window-size=1920,1080")
        opts.add_argument("start-maximized")
        opts.add_argument("disable-infobars")
        opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        return opts

    def _configParser(self):

        from configparser import ConfigParser

        config = ConfigParser()
        config.readfp(open(f"config.cfg"))

        browser_mode = config.get("Browser", "browser-mode")
        driver_path = config.get("Browser", "driver-path")
        browser_binary_location = config.get("Browser", "browser-binary-location")


        return (
            browser_mode,
            driver_path,
            browser_binary_location,
        )

    def quit(self):
        self.log.write_log("browser", 'Close Browser')
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            self.driver.close()

    def sleep(self, mins):

        import time

        self.log.write_log("bot", self.log.yellow_text(f"Sleeping for {mins} sec"))
        time.sleep(int(mins))

    def error_handler(self, msg):
        self.log.error_log(msg)

    def _click(self, element, msg="placeholder"):

        self.log.write_log("bot",f"clicking on {msg}")
        self.driver.find_element_by_xpath(element).click()

    def _random_wait(self, t_min, t_max):

        import time
        import random

        random_time = random.randrange(t_min, t_max)
        # self.log.write_log("bot", f"Waiting for {random_time} sec")
        time.sleep(random_time)


    def __get_xpath_elem(self, element):

        try:
            return self.driver.find_element_by_xpath(element)
        except Exception as e:
            self.log.write_log("warning", e)
            self.error_handler(e)
            pass

