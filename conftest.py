import json
import os
from datetime import datetime
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def context(request):
    context.options = Options()

    context.options.add_argument("--start-maximized")
    if os.getenv("CI"):
        context.options.add_argument("--headless=new")

    context.driver = webdriver.Chrome(options=context.options)
    with open("config.json", "r") as file:
        data = json.load(file)["page"]
    url = data["url"]
    if "user_id" in data:
        url = url + "/?user-id=" + data["user_id"]

    context.driver.get(url)

    request.node.driver = context.driver

    yield context

    context.driver.quit()

@pytest.fixture(scope="function")
def context_api(request):
    with open("config.json", "r") as file:
        data = json.load(file)["api"]
    context_api.base_url = data["url"]
    if "user_id" in data:
        context_api.header = {"x-user-id" : data["user_id"]}
    yield context_api




@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['context'].driver
            if driver:
                attach_screenshot(driver=driver)
        except KeyError:
            pass

def attach_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"{name}_{timestamp}",
        attachment_type=allure.attachment_type.PNG
    )
