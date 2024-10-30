import re

from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto(
        "http://192.168.111.232:18901/login?haveWarehouse=1&client_id=iowtb-new&redirect_uri=http://192.168.111.232:9832/login")
    page.get_by_placeholder("请输入账号").click()
    page.get_by_placeholder("请输入账号").fill("lhb001")
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill("lhx7758521")
    page.get_by_role("button", name="登录").click()
    expect(page.locator("header")).to_contain_text("首页")


