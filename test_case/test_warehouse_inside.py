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


class TestWarehouseInside:

    def test_warehouse_lock_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("li").filter(has_text="库存锁定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("li").filter(has_text="库存锁定").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("锁定类型").click()
        logged_in_page.get_by_title("常规锁定").click()
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("ui测试用")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator(".vxe-cell > .vxe-cell--checkbox > .vxe-checkbox--icon").click()
        logged_in_page.get_by_role("button", name="删 除").nth(1).click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_text("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("库区").click()
        logged_in_page.get_by_title("零货库区").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(".ag-cell-focus > .ag-cell-wrapper > .ag-selection-checkbox").click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator("td:nth-child(11) > .vxe-cell").click()
        logged_in_page.get_by_role("row", name=" M12321321 氨糖 9093281111 01").get_by_role("textbox").fill("0.001")
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="确 定").press("ArrowRight")
        logged_in_page.locator(".vxe-table--body-wrapper").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="审 核").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("已审核")

    def test_warehouse_un_lock_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("li").filter(has_text="库存解锁").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("解锁类型").click()
        logged_in_page.get_by_title("常规解锁").click()
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("库区").click()
        logged_in_page.get_by_title("整件库区").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        logged_in_page.locator("span").filter(has_text="整件库区").first.click()
        logged_in_page.get_by_title("零货库区").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator("td:nth-child(9) > .vxe-cell").click()
        logged_in_page.locator("td:nth-child(10)").dblclick()
        logged_in_page.locator("td:nth-child(10) > .vxe-cell").click()
        logged_in_page.locator("div").filter(has_text="新增库存解锁单产品类型药品货主智汇奇策科技有限公司").nth(
            1).press(
            "ArrowRight")
        logged_in_page.get_by_role("cell", name="计划解锁数量  ").locator("div").nth(1).click()
        logged_in_page.locator("td:nth-child(11) > .vxe-cell").click()
        logged_in_page.get_by_role("row", name="M12321321 氨糖 9093281111 01").get_by_role("textbox").fill("0.001")
        logged_in_page.locator(".vxe-table--body-wrapper").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("li").filter(has_text="库存解锁").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="审 核").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()

    def test_replenish_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("li").filter(has_text="补货管理").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("li").filter(has_text="补货管理").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").locator("div").click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("ui测试用数据")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(2)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("cell", name="请输入").locator("div").nth(3).click()
        logged_in_page.get_by_title("LH0020").click()
        logged_in_page.locator(".vxe-table--body-wrapper").first.click()
        logged_in_page.locator("td:nth-child(18) > .vxe-cell").click()
        logged_in_page.get_by_role("row", name="M12321321 氨糖 9093281111 01").get_by_role("textbox").fill("1")
        logged_in_page.get_by_label("备注").click()
        time.sleep(0.5)
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="下 发").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()

    def test_warehouse_location_change_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^移库管理$")).click()
        logged_in_page.locator("li").filter(has_text="移库单").nth(1).click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^移库管理$")).click()
        logged_in_page.locator("li").filter(has_text="移库单").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").locator("div").click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("ui测试用")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.locator(
            ".ant-form-item-control-input-content > div > .ant-select > .ant-select-selector > .ant-select-selection-overflow").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("来源库区").click()
        logged_in_page.get_by_title("零货库区").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        logged_in_page.get_by_label("来源货位").click()
        logged_in_page.get_by_label("来源货位").fill("LH0009")
        logged_in_page.get_by_title("LH0009").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(
            "div:nth-child(5) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("cell", name="* 请输入").locator("div").nth(3).click()
        logged_in_page.get_by_title("LH0020").click()
        logged_in_page.locator("td:nth-child(9) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name="  计划移动件数/数量不能为空").get_by_role("textbox").fill("0.001")
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()

    def test_location_change_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^移库管理$")).click()
        logged_in_page.locator("li").filter(has_text="移位管理").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").locator("div").click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("UI测试用")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        time.sleep(5)
        logged_in_page.locator(
            ".ant-form-item-control-input-content > div > .ant-select > .ant-select-selector").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("货位", exact=True).click()
        logged_in_page.get_by_label("货位", exact=True).fill("LH0009")
        logged_in_page.get_by_title("LH0009").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(5)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("cell", name="* 请输入").locator("div").nth(3).click()
        logged_in_page.locator("#rc_select_16").fill("LH0020")
        logged_in_page.get_by_title("LH0020").click()
        logged_in_page.locator("td:nth-child(16) > .vxe-cell").click()
        logged_in_page.get_by_role("row", name="M12321321 氨糖 9093281111 01").get_by_role("textbox").fill("0.001")
        logged_in_page.get_by_role("cell", name="* 请输入").locator("div").nth(3).click()
        logged_in_page.locator("#rc_select_16").fill("LH0020")
        logged_in_page.get_by_title("LH0020").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("创建人")).to_have_value("李鸿宾");
        logged_in_page.locator("div").filter(has_text=re.compile(r"^移库管理$")).click()
        logged_in_page.locator("li").filter(has_text="移位管理").nth(1).click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="下 发").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("已完成")

    def test_stock_mission_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^盘点管理$")).click()
        logged_in_page.locator("li").filter(has_text="盘点任务").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("盘点类型").click()
        logged_in_page.get_by_title("标准盘点").click()
        logged_in_page.get_by_label("产品类型").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("盘点方式").click()
        logged_in_page.get_by_title("纸质").click()
        logged_in_page.get_by_label("明盘").click()
        logged_in_page.get_by_title("否").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="删 除").click()
        logged_in_page.get_by_role("button", name="确 定").click()

    def test_stock_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^盘点管理$")).click()
        logged_in_page.locator("li").filter(has_text="盘点").nth(2).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.locator("span").filter(has_text="RF").click()
        logged_in_page.get_by_title("纸质").first.click()
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        time.sleep(8)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="盘点单打印").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")
        logged_in_page.locator("div").filter(has_text=re.compile(r"^盘点管理$")).click()
        logged_in_page.locator("li").filter(has_text="盘点").nth(2).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        time.sleep(1)
        logged_in_page.locator("li").filter(has_text="盘点").nth(2).click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="盘点完成").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_stock_change_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^盘盈盘亏$")).click()
        logged_in_page.locator("li").filter(has_text="盘盈盘亏 盘盈盘亏单").get_by_role("listitem").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("货权组织").click()
        logged_in_page.get_by_title("零售事业部").click()
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(
            "div:nth-child(4) > .ag-root-wrapper > .ag-root-wrapper-body > .ag-root > .ag-body-viewport > .ag-pinned-left-cols-container > div > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator("td:nth-child(8) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name=" 请输入调整原因").get_by_role("textbox").click()
        logged_in_page.get_by_text("原箱差异").click()
        logged_in_page.locator("td:nth-child(12) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name="  请输入调整件数/数量").get_by_role("textbox").fill("1")
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("ui测试用")
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="审 核").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()

    def test_hc_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^耗材$")).click()
        logged_in_page.locator("li").filter(has_text="耗材分类").nth(1).click()
        logged_in_page.get_by_role("button", name="新增平级").click()
        logged_in_page.get_by_label("分类编码").click()
        logged_in_page.get_by_label("分类编码").fill("testui")
        logged_in_page.get_by_label("分类名称", exact=True).click()
        logged_in_page.get_by_label("分类名称", exact=True).fill("UI测试用")
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("UI测试用")
        logged_in_page.get_by_role("button", name="保 存").click()
        logged_in_page.get_by_text("UI测试用").click()
        logged_in_page.get_by_role("button", name="删 除").click()
        logged_in_page.get_by_role("button", name="确 定").click()

    def test_hc_management_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^耗材$")).click()
        logged_in_page.locator("li").filter(has_text="耗材管理").nth(1).click()
        logged_in_page.get_by_role("button", name="查看").first.click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.get_by_role("button", name="编辑").first.click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="库存调整").first.click()
        logged_in_page.get_by_label("变动属性").click()
        logged_in_page.get_by_text("增", exact=True).click()
        logged_in_page.get_by_role("spinbutton", name="请输入").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").fill("1")
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()

    def test_process_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^加工计费$")).click()
        logged_in_page.locator("li").filter(has_text="加工报价合同").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("合同编号").click()
        logged_in_page.get_by_label("合同编号").fill("testui")
        logged_in_page.get_by_label("合同开始时间").click()
        logged_in_page.get_by_title("-10-01").locator("div").click()
        logged_in_page.get_by_label("合同到期时间").click()
        logged_in_page.get_by_role("cell", name="31").nth(1).click()
        logged_in_page.get_by_label("合同签订时间").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(2).click()
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("testui")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("指令简称").click()
        logged_in_page.get_by_label("指令简称").fill("1")
        logged_in_page.get_by_label("指令名称").click()
        logged_in_page.get_by_label("指令名称").fill("1")
        logged_in_page.get_by_role("spinbutton", name="请输入").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").fill("1")
        logged_in_page.get_by_role("textbox", name="请输入").click()
        logged_in_page.get_by_role("textbox", name="请输入").fill("1")
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.locator("#app").get_by_role("button", name="删 除").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="查看").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^加工计费$")).click()
        logged_in_page.locator("li").filter(has_text="加工报价合同").nth(1).click()


    def test_process_command_order_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^加工计费$")).click()
        logged_in_page.locator("li").filter(has_text="加工指令单").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("组织").click()
        logged_in_page.get_by_title("零售事业部").click()
        logged_in_page.get_by_label("计划开始时间").click()
        logged_in_page.get_by_title("-10-01").locator("div").click()
        logged_in_page.locator("li").filter(has_text="确 定").get_by_role("button").click()
        logged_in_page.get_by_label("计划结束时间").click()
        logged_in_page.get_by_role("cell", name="31").click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.get_by_label("产品", exact=True).click()
        logged_in_page.get_by_label("产品", exact=True).fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").fill("1")
        logged_in_page.get_by_role("button", name="新 增").nth(1).click()
        logged_in_page.get_by_label("加工指令", exact=True).click()
        logged_in_page.get_by_title("加工单").click()
        logged_in_page.get_by_role("textbox", name="请输入").click()
        logged_in_page.get_by_role("textbox", name="请输入").fill("UI测试用")
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="审 核").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="完工登记").first.click()
        logged_in_page.get_by_label("实际开始时间").click()
        logged_in_page.get_by_role("dialog").get_by_title("-10-01").locator("div").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_label("实际结束时间").click()
        logged_in_page.get_by_role("cell", name="31").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("combobox", name="* 加工指令").click()
        logged_in_page.get_by_role("dialog").get_by_title("加工单").click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.get_by_label("作业人员").fill("李鸿宾")
        logged_in_page.locator("[id=\"\\31 804053224903168\"]").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").nth(1).click()
        logged_in_page.get_by_role("spinbutton", name="请输入").nth(1).fill("1")
        logged_in_page.get_by_role("textbox", name="请输入").click()
        logged_in_page.get_by_role("textbox", name="请输入").fill("UI测试用")
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.locator("#app").get_by_role("button", name="删 除").click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()


    def test_process_settlement_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^加工计费$")).click()
        logged_in_page.locator("li").filter(has_text="加工结算单").nth(1).click()
        logged_in_page.locator(".ag-cell-wrapper").first.click()
        logged_in_page.get_by_role("button", name="计 算").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="生成账单", exact=True).click()
        logged_in_page.get_by_label("结算年月").click()
        logged_in_page.get_by_role("cell", name="1月", exact=True).click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="查看").first.click()
        expect(logged_in_page.get_by_label("货主")).to_have_value("智汇奇策科技有限公司");
        logged_in_page.locator("div").filter(has_text=re.compile(r"^加工计费$")).click()
        logged_in_page.locator("li").filter(has_text="加工结算单").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()


    def test_down_shelf_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("li").filter(has_text="PC下架").click()
        logged_in_page.get_by_role("button", name="下架索取(F1)").click()
        logged_in_page.get_by_role("row", name=" 1").get_by_role("cell").first.click()
        logged_in_page.get_by_role("button", name="一键下架(F6)").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("cell", name="").nth(1).click()
        logged_in_page.get_by_role("button", name="补打下架标签(F2)").click()
        logged_in_page.get_by_label("下架类型").click()
        logged_in_page.get_by_title("补货下架").click()
        logged_in_page.get_by_title("全选/取消").locator("span").click()
        logged_in_page.get_by_role("button", name="一键下架(F6)").click()
        logged_in_page.get_by_role("button", name="确 定").click()


    def test_down_shelf_list_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="库内管理").click()
        logged_in_page.locator("li").filter(has_text="下架任务列表").click()
        logged_in_page.get_by_role("row", name="1", exact=True).locator("div").dblclick()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
