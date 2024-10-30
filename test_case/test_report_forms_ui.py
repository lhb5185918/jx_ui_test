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


class TestReportFormsUi:

    def test_location_select_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^仓库快捷查询$")).click()
        logged_in_page.locator("li").filter(has_text="仓库快捷查询 货位快捷查询").get_by_role("listitem").click()
        logged_in_page.locator(
            "div:nth-child(2) > .flex > .flex-1 > .ant-select > .ant-select-selector > .ant-select-selection-overflow").click()
        logged_in_page.get_by_title("零货库区").click()
        logged_in_page.get_by_placeholder("请输入").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).fill("LH0009")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("01零货库区")

    def test_inventory_container_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库存容器").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow-item").click()
        logged_in_page.locator("#rc_select_5").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("20240910001")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("氨糖")

    def test_inventory_total_price_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库存总账").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow-item").first.click()
        logged_in_page.locator("#rc_select_5").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.locator(
            "div:nth-child(4) > .flex > .flex-1 > .ant-select > .ant-select-selector > .ant-select-selection-overflow > .ant-select-selection-overflow-item").click()
        logged_in_page.get_by_title("合格", exact=True).click()
        logged_in_page.get_by_role("gridcell", name="维生素A").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("氨糖")

    def test_inventory_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库存明细").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow-item").click()
        logged_in_page.locator("#rc_select_5").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("td:nth-child(6) > .vxe-cell > .vxe-cell--label").first).to_be_visible()
        expect(logged_in_page.locator("#app")).to_contain_text("氨糖")

    def test_inventory_flowing_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库存交易流水").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_5").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("氨糖")

    def test_inventory_years_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库龄分析").nth(1).click()
        logged_in_page.locator(
            ".flex-1 > div > .ant-select > .ant-select-selector > .ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_7").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("氨糖")

    def test_inventory_status_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库存$")).click()
        logged_in_page.locator("li").filter(has_text="库存状态变更").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow-item").first.click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("氨糖")

    def test_in_order_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库订单明细表").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^订单类型$")).nth(2).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.get_by_title("采购订单", exact=True).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_in_order_resave_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库收货明细表").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^收货员$")).nth(2).click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("李鸿宾")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_in_order_check_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库验收明细表").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^批号$")).nth(2).click()
        logged_in_page.get_by_placeholder("请输入").nth(2).click()
        logged_in_page.get_by_placeholder("请输入").nth(2).fill("20240910001")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("验收完成")

    def test_in_order_put_shelf_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库上架明细表").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_5").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_order_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库单明细表").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^批号$")).nth(2).click()
        logged_in_page.get_by_placeholder("请输入").nth(2).click()
        logged_in_page.get_by_placeholder("请输入").nth(2).fill("20240910001")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_in_order_work_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库订单作业汇总").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^业务类型$")).nth(2).click()
        logged_in_page.locator("#rc_select_8").click()
        logged_in_page.get_by_title("ToB").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_in_order_monitor_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^入库报表$")).click()
        logged_in_page.locator("li").filter(has_text="入库监控").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^供应商$")).first.click()
        logged_in_page.locator("#rc_select_10").click()
        logged_in_page.get_by_title("青岛医药科技集团有限公司--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("td:nth-child(3) > .vxe-cell > .vxe-cell--label").first).to_be_visible()

    def test_warehouse_inside_hc_record_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="耗材库存记录").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).fill("玻璃瓶")
        logged_in_page.locator("td:nth-child(2) > .vxe-cell").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_placeholder("请输入").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).fill("自动化测试")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("tbody")).to_contain_text("自动化测试耗材")

    def test_warehouse_inside_hz_record_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="货转明细记录").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_warehouse_replenish_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="补货记录报表").nth(1).click()
        logged_in_page.locator("form").get_by_text("业务类型").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^补货类型$")).nth(2).click()
        logged_in_page.locator("#rc_select_9").click()
        logged_in_page.get_by_title("主动补货").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("主动补货")

    def test_warehouse_stock_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="库存锁定记录").nth(1).click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.get_by_title("已审核").locator("div").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("已审核")

    def test_warehouse_inside_un_stock_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="库存解锁记录").nth(1).click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.get_by_title("已审核").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("常规解锁")

    def test_warehouse_inside_move_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="移库明细记录").nth(1).click()
        logged_in_page.locator("#rc_select_5").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("李鸿宾")

    def test_location_move_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="移位明细记录").nth(1).click()
        logged_in_page.locator("#rc_select_5").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_warehouse_bhg_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="不合格报损明细").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_warehouse_stocktaking_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^库内报表$")).click()
        logged_in_page.locator("li").filter(has_text="盘盈盘亏报表").nth(1).click()
        logged_in_page.locator("#rc_select_5").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("手工创建")

    def test_out_order_allocation_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="出库订单分配明细").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_7").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.locator(".vxe-cell--label").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("氨糖")

    def test_out_order_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="出库订单明细").nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_7").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.locator("td:nth-child(2) > .vxe-cell").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("氨糖")

    def test_channel_out_order_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="取消订单明细").nth(1).click()
        logged_in_page.locator("#rc_select_3").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_out_order_pick_detail_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="拣货明细").nth(1).click()
        logged_in_page.locator(".flex-1 > .ant-select > .ant-select-selector").first.click()
        logged_in_page.get_by_title("ToB").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("李鸿宾")

    def test_out_order_fh_schedule_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="分拣复核进度").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^SO状态$")).nth(2).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.get_by_title("生成波次").locator("div").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("生成波次")

    def test_out_order_pick_schedule_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="拣货进度").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^拣货员$")).nth(1).click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("李鸿宾")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("tbody")).to_contain_text("李鸿宾")

    def test_out_order_work_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="出库作业记录").nth(1).click()
        logged_in_page.locator(".flex-1 > .ant-select > .ant-select-selector").first.click()
        logged_in_page.locator("[id=\"\\31 770570116141568\"]").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("tbody")).to_contain_text("李鸿宾")

    def test_out_order_frequency_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="出库频次查询").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("tbody")).to_contain_text("氨糖")

    def test_out_order_statistic_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="发货统计").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("#app")).to_contain_text("智汇奇策科技有限公司")

    def test_out_order_monitor_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="报表").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^出库报表$")).click()
        logged_in_page.locator("li").filter(has_text="发货监控").nth(1).click()
        logged_in_page.locator("#rc_select_5").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator(".ant-table-row > td:nth-child(3)").first).to_be_visible()
