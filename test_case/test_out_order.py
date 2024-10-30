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


class TestOrderOutPage:

    def test_so_fp_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("p").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="SO分配").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="分 配").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".ag-row-odd > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="分 配").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToC");
        logged_in_page.locator("li").filter(has_text="SO分配").click()
        logged_in_page.locator(".ag-row-odd > .ag-cell-value > .action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToB");
        logged_in_page.locator("li").filter(has_text="SO分配").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()

    def test_so_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="SO").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_role("grid")).to_contain_text("全部分配")
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToC");
        logged_in_page.locator("li").filter(has_text="SO").first.click()
        logged_in_page.locator(".ag-row-odd > .ag-cell-value > .action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToB");
        logged_in_page.locator("li").filter(has_text="SO").first.click()
        logged_in_page.locator(".ag-row-odd > div > .ag-cell-wrapper > .ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="修改承运商").click()
        logged_in_page.get_by_label("提货方式").click()
        logged_in_page.get_by_text("自配送").click()
        logged_in_page.get_by_label("承运商", exact=True).click()
        logged_in_page.get_by_text("青岛测试集团托运公司").click()
        logged_in_page.get_by_role("button", name="确 认").click()

    def test_wave_xf_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="波次下发").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="波次安排(F1)").click()
        logged_in_page.get_by_text("只拣不播").first.click()
        logged_in_page.get_by_title("先拣后播").click()
        logged_in_page.locator("span").filter(has_text="只拣不播").click()
        logged_in_page.get_by_title("先拣后播").nth(2).click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("gridcell", name="Press Space to toggle row").locator("div").nth(1).click()
        logged_in_page.get_by_role("button", name="波次安排(F1)").click()
        logged_in_page.get_by_text("只拣不播").first.click()
        logged_in_page.get_by_title("先拣后播").first.click()
        logged_in_page.locator("span").filter(has_text="只拣不播").click()
        logged_in_page.get_by_title("先拣后播").nth(2).click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.locator("#rc-tabs-1-tab-2").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="波次发布").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="关 闭").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="波次发布").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="关 闭").click()
        logged_in_page.get_by_role("gridcell", name="药品").first.click()
        logged_in_page.get_by_role("cell", name="否", exact=True).locator("div").click()
        logged_in_page.get_by_role("textbox").click()
        logged_in_page.get_by_text("是", exact=True).click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="波次发布").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="关 闭").click()

    def test_wave_list_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="波次列表").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToC");
        logged_in_page.locator("li").filter(has_text="波次列表").click()
        logged_in_page.locator(".ag-row-odd > .ag-cell-value > .action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("业务类型")).to_have_value("ToB");
        logged_in_page.locator("li").filter(has_text="波次列表").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_pick_list_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="拣货单列表").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("li").filter(has_text="拣货单列表").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="打 印").click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_label("拣货员").click()
        logged_in_page.get_by_label("拣货员").fill("李鸿宾")
        logged_in_page.locator("[id=\"\\31 804053224903168\"]").get_by_text("李鸿宾").click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="确认").click()
        logged_in_page.locator(".ag-row-odd > .ag-cell-value > .action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_label("拣货员").click()
        logged_in_page.get_by_label("拣货员").fill("李鸿宾")
        logged_in_page.locator("[id=\"\\31 804053224903168\"]").get_by_text("李鸿宾").click()
        logged_in_page.get_by_role("button", name="确 认").click()
        logged_in_page.get_by_role("button", name="确认").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_text("创建日期Fm创建日期To波次单号拣货单号").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_pick_mission_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="拣货单任务列表").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("产品表单类型")).to_have_value("药品");
        logged_in_page.locator("li").filter(has_text="拣货单任务列表").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="补打拣货任务").click()
        logged_in_page.get_by_role("button", name="补打分拣明细").click()
        logged_in_page.get_by_role("button", name="补打拣货纸单").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.get_by_role("button", name="搜索").first.click()

    def test_get_pick_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="PC拣货").click()
        logged_in_page.locator("div:nth-child(3) > div > .ag-cell-wrapper > .ag-selection-checkbox").click()
        logged_in_page.locator("div:nth-child(4) > div > .ag-cell-wrapper > .ag-selection-checkbox").click()
        logged_in_page.get_by_role("button", name="一键拣货").click()

    def test_lh_bz_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="拣货单任务列表").click()
        pick_mission_no = logged_in_page.locator(
            'xpath=//*[@id="app"]/section/section/section/div[3]/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/div[3]').inner_text()
        # pick_mission_no = logged_in_page.locator('xpath=//*[@id="app"]/section/section/section/div[3]/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[3]/div[3]').inner_text()
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="零货播种").click()
        logged_in_page.locator("div").filter(has_text=re.compile(
            r"^容器/拣货任务产品条码批号待分拣数量打印分拣单\(F6\)打印箱标签\(F1\)强制分拣\(F2\)应播数0已播数0$")).get_by_role(
            "textbox").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(
            r"^容器/拣货任务产品条码批号待分拣数量打印分拣单\(F6\)打印箱标签\(F1\)强制分拣\(F2\)应播数0已播数0$")).get_by_role(
            "textbox").first.fill(pick_mission_no)
        logged_in_page.locator("div").filter(has_text=re.compile(
            r"^容器/拣货任务产品条码批号待分拣数量打印分拣单\(F6\)打印箱标签\(F1\)强制分拣\(F2\)应播数0已播数0$")).get_by_role(
            "textbox").first.press("Enter")
        logged_in_page.get_by_role("gridcell", name="1", exact=True).dblclick()
        logged_in_page.locator("input[name=\"unSowQtyInput\"]").click()
        logged_in_page.locator("input[name=\"unSowQtyInput\"]").press("Enter")
        logged_in_page.get_by_role("button", name="拣货容器(F3)").click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.get_by_role("button", name="分拣信息(F4)").click()
        logged_in_page.get_by_role("button", name="取 消").click()
        logged_in_page.get_by_role("button", name="重置(F5)").click()

    def test_cl_fh_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="拣货单任务列表").click()
        logged_in_page.locator(".ag-row-odd > .ag-cell-value > .action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^播种信息$")).first.click()
        box_no = logged_in_page.locator(
            'xpath=/html/body/div[2]/section/section/section/div[3]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div[4]').inner_text()
        print(box_no)
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.get_by_text("出库").click()
        logged_in_page.locator("li").filter(has_text="拆零复核").click()
        logged_in_page.locator(".table_content > div > .ant-select-selector").click()
        logged_in_page.get_by_text("02", exact=True).click()
        logged_in_page.locator(".ant-input").first.click()
        logged_in_page.locator(".ant-input").first.fill(box_no)
        logged_in_page.locator(".ant-input").first.press("Enter")
        logged_in_page.get_by_role("gridcell", name="1", exact=True).dblclick()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^单位：规格：批号：20240910001复核数量：$")).get_by_role(
            "textbox").nth(2).click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^单位：规格：批号：20240910001复核数量：$")).get_by_role(
            "textbox").nth(2).press("Enter")
        logged_in_page.get_by_role("button", name="复核完成(F2)").click()

    def test_jh_fh_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.get_by_text("出库").click()
        logged_in_page.locator("li").filter(has_text="集货复核").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^未索取任务$")).first.click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="手工集货(F2)").click()
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^已索取任务$")).first.click()
        logged_in_page.get_by_role("button", name="索取(F1)").click()
        logged_in_page.get_by_role("gridcell", name="Press Space to toggle row").locator("div").nth(1).click()
        logged_in_page.get_by_role("button", name="一键复核(F4)").click()
        logged_in_page.get_by_role("button", name="确 定").click()

    def test_lh_bz_toc_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="拣货单任务列表").click()
        pick_no = logged_in_page.locator(
            'xpath=//*[@id="app"]/section/section/section/div[3]/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div[2]').inner_text()
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^ToC出库$")).click()
        logged_in_page.locator("li").filter(has_text="toc播种").nth(1).click()
        logged_in_page.locator("input[name=\"inputPickOrderNo\"]").click()
        logged_in_page.locator("input[name=\"inputPickOrderNo\"]").fill(pick_no)
        logged_in_page.locator("input[name=\"inputPickOrderNo\"]").press("Enter")
        logged_in_page.get_by_role("gridcell", name="1", exact=True).dblclick()
        logged_in_page.locator("input[name=\"inputUnSowQty\"]").click()
        logged_in_page.locator("input[name=\"inputUnSowQty\"]").press("Enter")

    def test_fh_toc_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("li").filter(has_text="SO").first.click()
        so_no = logged_in_page.locator(
            'xpath=//*[@id="app"]/section/section/section/div[3]/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div[1]').inner_text()
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="出库").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^ToC出库$")).click()
        logged_in_page.locator("li").filter(has_text="复核装箱").nth(1).click()
        logged_in_page.locator("#rc_select_1").click()
        logged_in_page.get_by_text("出库作业台").click()
        logged_in_page.locator("form").filter(has_text="SO单号").get_by_role("textbox").click()
        logged_in_page.locator("form").filter(has_text="SO单号").get_by_role("textbox").fill(so_no)
        logged_in_page.locator("form").filter(has_text="SO单号").get_by_role("textbox").press("Enter")
        time.sleep(0.5)
        logged_in_page.get_by_role("gridcell", name="1", exact=True).dblclick()
        time.sleep(0.5)
