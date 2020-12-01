from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from BmpProxy import ProxyManager

class ClientManager:

    def __init__(self):
        self.options = ChromeOptions()
        self.caps = DesiredCapabilities.CHROME
        self.proxy = ProxyManager()
        self.server = self.proxy.start_server()
        self.proxyClient = self.proxy.start_client()

    def setup(self):
        self.caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.options.add_argument("--proxy-server={0}".format(self.proxyClient.proxy))

    def start_capture(self):
        self.proxyClient.new_har('', options={'captureContent': True})

    @property
    def driver(self):
        return Chrome(options = self.options, desired_capabilities = self.caps)

    @property
    def client(self):
        return self.proxyClient


