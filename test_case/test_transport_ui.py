import pytest
import re
from playwright.sync_api import sync_playwright, Page, expect
import time
from other_utils import *
import asyncio


@pytest.fixture(scope="class")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 可视化模式
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        yield context
        # context.close()
        # browser.close()


@pytest.fixture(scope="class")
def logged_in_page(browser_context) -> Page:
    page = browser_context.new_page()
    page.goto(
        "http://192.168.111.232:18901/login?haveWarehouse=1&client_id=iowtb-new&redirect_uri=http://192.168.111.232:9832/login")
    page.get_by_placeholder("请输入账号").click()
    page.get_by_placeholder("请输入账号").fill("ssoadmintest6")
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill("lhx7758521")
    page.locator("#warehouse").select_option("1")
    page.get_by_role("button", name="登录").click()
    expect(page.locator("header")).to_contain_text("首页")
    yield page
    # page.close()


class TestTransportUi:

    def test_delivery_car_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="配送管理").click()
        logged_in_page.locator("li").filter(has_text="配送排车").click()
        logged_in_page.locator(
            "div:nth-child(7) > .ant-row > div:nth-child(2) > .ant-form-item-control-input > .ant-form-item-control-input-content > .ant-select > .ant-select-selector").click()
        # 找到特定元素
        element = logged_in_page.locator(
            'xpath=//*[@id="rc-tabs-1-panel-1"]/div/div[1]/div[1]/div[1]/form/div/div[7]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[1]')  # 替换为实际的选择器
        # 将鼠标移动到该元素上
        element.scroll_into_view_if_needed()  # 确保元素在视口内
        # 滚动
        element.evaluate("el => el.scrollTop += 1000")  # 向下滚动 100 像素
        logged_in_page.get_by_title("全部集货复核").locator("div").click()
        logged_in_page.get_by_role("tab", name="已排单").click()
        logged_in_page.get_by_role("button", name="新装车单(F7)").click()
        logged_in_page.get_by_role("cell", name="").nth(1).click()
        logged_in_page.get_by_role("tab", name="未排单").click()
        logged_in_page.get_by_role("cell", name="").nth(1).click()
        logged_in_page.get_by_role("button", name="加单(F3)").click()
        logged_in_page.get_by_role("tab", name="已排单").click()

    def test_delivery_car_issued_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="配送管理").click()
        logged_in_page.locator("li").filter(has_text="配送装车下发").click()
        logged_in_page.get_by_role("row", name=" 1").locator("div").nth(1).dblclick()
        logged_in_page.get_by_label("车牌号").click()
        logged_in_page.get_by_title("鲁bqp01").click()
        logged_in_page.get_by_label("配送司机").click()
        logged_in_page.get_by_text("测试司机").click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("cell", name="").nth(1).click()
        logged_in_page.get_by_role("button", name="下发(F1)").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("tab", name="已下发装车单").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_delivery_car_check_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="配送管理").click()
        logged_in_page.locator("li").filter(has_text="配送装车确认").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="直接确认(F2)").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()

    def test_deliver_car_back_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="配送管理").click()
        logged_in_page.locator("li").filter(has_text="配送返回").click()
        logged_in_page.locator(".ag-row-even > div:nth-child(2)").first.click()
        logged_in_page.get_by_role("button", name="修改数量").click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="附件").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_role("cell", name="文件名1").locator("div").click()
        logged_in_page.get_by_label("附件").get_by_role("textbox").fill("UI测试用")
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.get_by_role("button", name="返单确认(F10)").click()
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-header > .ag-pinned-left-header > .ag-header-row > div").first.click()
        logged_in_page.get_by_role("button", name="返单确认(F10)").click()
