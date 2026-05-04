from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserDriver:
    def __init__(self, headless=False):
        self.options = Options()
        self._setup_options(headless)
        self.driver = webdriver.Chrome(options=self.options)

    def _setup_options(self, headless):
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        # СКОРОСТЬ
        self.options.page_load_strategy = "eager"

        # ОТКЛЮЧАЕМ КАРТИНКИ
        prefs = {
            "profile.managed_default_content_settings.images": 2,
        }
        self.options.add_experimental_option("prefs", prefs)

        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )

        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        self.options.add_experimental_option("useAutomationExtension", False)

        if headless:
            self.options.add_argument("--headless=new")

    def get(self, url):
        self.driver.get(url)

    def quit(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()