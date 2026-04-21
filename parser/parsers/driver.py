from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserDriver:
    def __init__(self, headless=True):
        self.options = Options()
        self._setup_options(headless)
        self.driver = webdriver.Chrome(options=self.options)
    
    def _setup_options(self, headless):
        """Настройка опций браузера для Selenium"""
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        
        # SSL / безопасность
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--ignore-ssl-errors=yes")
        self.options.add_argument("--allow-insecure-localhost")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        # User-Agent (имитирует обычный Chrome)
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/124.0.0.0 Safari/537.36")

        # Убираем лишние логи и автоматизацию
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.options.add_experimental_option("useAutomationExtension", False)

        # Headless режим
        if headless:
            self.options.add_argument("--headless=new")  # Для Chrome 109+
    
    def get(self, url):
        """Открыть страницу"""
        self.driver.get(url)
    
    def quit(self):
        """Закрыть браузер"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие при выходе из контекста"""
        self.quit()