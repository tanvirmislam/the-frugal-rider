import platform
import time
import traceback

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
from typing import List


class Driver(object):

    def __init__(self) -> None:
        self.chrome = None
        self.is_headless = None
        self.delay_after_view_change = 0.2
        self.page_load_check_interval = 0.2

    def init_driver(self, is_headless: bool, width: int, height: int) -> bool:
        """
        This function initializes the driver variable

        :param is_headless: True if running in headless mode, False otherwise
        :param width: Chrome window width
        :param height: Chrome window height
        :return:
        """

        self.is_headless = is_headless

        # ------------------------------------------------------------------
        # Detect system and locate appropriate chromedriver executable file
        # ------------------------------------------------------------------
        system_switcher = {
            'darwin': 'mac',
            'windows': 'windows',
            'linux': 'linux'
        }

        system_name = system_switcher.get(platform.system().lower(), None)
        ext = ''
        if system_name is None:
            print('Invalid platform')
            return False
        elif system_name == 'windows':
            ext = '.exe'

        # Chromedriver version
        version = '79'

        driver_file_name = system_name + '_chromedriver_' + version + ext
        exec_path = Path.cwd() / 'util' / 'chromedriver/' / driver_file_name
        print(exec_path)

        if (not exec_path.exists()) or (not exec_path.is_file()):
            print('Chromedriver file not found')
            return False

        # -------------------
        # Set driver options
        # -------------------
        options = Options()

        if is_headless:
            options.headless = True
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        else:
            options.headless = False

        options.add_argument('--enable-popup-blocking')
        options.add_argument('disable-infobars')
        options.add_argument('disable-notifications')
        options.add_argument('log-level=3')

        options.add_argument('window-size=' + str(width) + ',' + str(height))

        if system_name == "windows":
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--kiosk")

        # ----------------------------------
        # Initialize the driver instance
        # ----------------------------------
        try:
            self.chrome = webdriver.Chrome(options=options, executable_path=str(exec_path))
            if is_headless is True:
                self.chrome.set_window_size(width, height)
        except selenium.common.exceptions.WebDriverException:
            print(
                '\n=================================\n'
                'Error: Incompatible chromedriver\n'
                '\n=================================\n'
            )
            return False

        return True


    def get_url(self, url: str) -> None:
        self.chrome.get(url)


    def get_element(self, fetch_method: By, specifier: str) -> WebElement:
        return self.chrome.find_element(fetch_method, specifier)


    def get_elements(self, fetch_method: By, specifier: str) -> List[WebElement]:
        return self.chrome.find_elements(fetch_method, specifier)


    def get_relative_element(self, parent_element: WebElement, fetch_method: By, specifier: str) -> WebElement:
        return parent_element.find_element(fetch_method, specifier)


    def get_relative_elements(self, parent_element: WebElement, fetch_method: By, specifier: str) -> List[WebElement]:
        return parent_element.find_elements(fetch_method, specifier)


    def get_html_element(self) -> WebElement:
        return self.get_element(By.TAG_NAME, 'html')


    def scroll_element_into_view(self, element: WebElement) -> None:
        self.chrome.execute_script(Driver.get_scroll_into_view_command(), element)
        time.sleep(self.delay_after_view_change)


    def move_to_element(self, element: WebElement) -> None:
        ActionChains(self.chrome).move_to_element(element).perform()
        time.sleep(self.delay_after_view_change)


    def press_key(self, key: Keys):
        ActionChains(self.chrome).send_keys(key).perform()


    def fill_text(self, text_element: WebElement, text: str) -> None:
        text_element.send_keys(text)


    def wait_till_page_load(self, old_html_element: WebElement) -> None:
        while self.get_element(By.TAG_NAME, 'html') == old_html_element:
            time.sleep(self.page_load_check_interval)


    def quit(self) -> None:
        self.chrome.quit()


    @staticmethod
    def get_scroll_into_view_command() -> str:
        js_cmd = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" + \
                 "var elementTop = arguments[0].getBoundingClientRect().top;" + \
                 "window.scrollBy(0, elementTop-(viewPortHeight/3));"
        return js_cmd

    @staticmethod
    def print_failure(excp: Exception):
        print(
            '\n======================================================\n'
            'Error: failure occurred during WebDriver navigation'
            '\n======================================================\n'
        )
        print(str(excp))
        traceback.print_exc()
        print('======================================================\n')


    # Static variable
    failure_exceptions = (
        AttributeError, TypeError, ValueError, LookupError, RuntimeError,
        selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementClickInterceptedException,
        selenium.common.exceptions.InvalidSelectorException, selenium.common.exceptions.NoSuchFrameException,
        selenium.common.exceptions.ElementNotVisibleException, selenium.common.exceptions.NoSuchAttributeException,
        selenium.common.exceptions.ElementNotSelectableException, selenium.common.exceptions.WebDriverException,
        selenium.common.exceptions.StaleElementReferenceException, selenium.common.exceptions.TimeoutException
    )


