from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver.driver
        self.wait = WebDriverWait(driver.driver, timeout)

    def wait_for_visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_invisibility(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def element_present(self, xpath):
        try:
            self.finds_element(xpath)
            return True
        except:
            return False

    def finds_element(self, locator):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", self.driver.find_element(locator[0], locator[1]))
        return self.driver.find_element(locator[0], locator[1])


    @staticmethod
    def format_locator(xpath: str, params: dict[str, str]):
        formatted_xpath = xpath[1].format(**params)
        return (By.XPATH, formatted_xpath)
