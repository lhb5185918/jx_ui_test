import pytest
import re
from playwright.sync_api import sync_playwright, Page, expect
import time
from other_utils import *
import requests


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


@pytest.fixture(scope="class")
def login_session():
    url = "http://192.168.111.232:17777/oauth/password/unencrypted"
    data = {
        "userNo": "lhb001",
        "pwd": "lhx7758521",
        "platForm": "app",
        "companyCode": "ZHQC",
        "whId": 1,
        "warehouseId": "",
        "haveWarehouse": 1,
        "clientId": "iowtb-new",
        "userLanguage": "zh-CN"
    }
    res = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = res.json()['obj']['token']
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    return headers


class TestGspManagement:

    def test_product_status_change_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("li").filter(has_text="产品状态变化").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_label("变化类型").click()
        logged_in_page.get_by_title("合格转待处理").click()
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        time.sleep(3)
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("库区").click()
        logged_in_page.get_by_title("零货库区").locator("div").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(2)
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.locator("td:nth-child(13) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name="  调整数量必须填写").get_by_role("textbox").fill("0.001")
        logged_in_page.locator("td:nth-child(14) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name=" 变更原因必须填写").get_by_role("textbox").click()
        logged_in_page.get_by_text("超有效期").click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("创建人")).to_have_value("李鸿宾");
        logged_in_page.locator("li").filter(has_text="产品状态变化").click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()

    def test_yh_check_list_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="养护确定表").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("货主")).to_have_value("智汇奇策科技有限公司");
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="养护确定表").nth(1).click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="养护确定表").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").locator("div").click()
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        logged_in_page.get_by_label("Close", exact=True).nth(1).click()
        logged_in_page.get_by_title("一般养护").click()
        logged_in_page.get_by_title("重点养护").click()
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("金嗓子喉宝")
        logged_in_page.get_by_title("金嗓子喉宝--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.get_by_role("button", name="确 定").first.click()

    def test_yh_record_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="产品养护记录单").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_role("button", name="添加明细").click()
        logged_in_page.get_by_label("Close", exact=True).nth(1).click()
        logged_in_page.get_by_title("一般养护").click()
        logged_in_page.get_by_title("重点养护").locator("div").click()
        logged_in_page.get_by_role("button", name="添加明细").click()
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.get_by_role("cell", name=" 养护措施必须填写").get_by_role("textbox").click()
        logged_in_page.get_by_text("防鼠").click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="产品养护记录单").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_yh_files_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^养护管理$")).click()
        logged_in_page.locator("li").filter(has_text="产品养护档案").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("gridcell", name="1", exact=True).click()
        logged_in_page.get_by_role("button", name="打 印").click()

    def test_quality_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^质量复检管理$")).click()
        logged_in_page.locator("li").filter(has_text="质量复检通知单").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("UI测试用")
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        time.sleep(3)
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.locator("td:nth-child(13) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name="  复检数量必须填写").get_by_role("textbox").fill("0.001")
        logged_in_page.locator("td:nth-child(14) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name=" 复检原因必须填写").get_by_role("textbox").click()
        logged_in_page.get_by_text("超有效期").click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("创建人")).to_have_value("李鸿宾");
        logged_in_page.locator("div").filter(has_text=re.compile(r"^质量复检管理$")).click()
        logged_in_page.locator("li").filter(has_text="质量复检通知单").nth(1).click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()

    def test_quality_audit_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^质量复检管理$")).click()
        logged_in_page.locator("li").filter(has_text="质量复检审核").nth(1).click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^质量复检管理$")).click()
        logged_in_page.locator("li").filter(has_text="质量复检审核").nth(1).click()
        logged_in_page.locator(".action_btn > div:nth-child(2) > .ant-btn").first.click()
        expect(logged_in_page.get_by_label("创建人")).to_have_value("李鸿宾");
        logged_in_page.locator("td:nth-child(16) > .vxe-cell").click()
        logged_in_page.get_by_role("cell", name=" 请输入复检结果").get_by_role("textbox").click()
        logged_in_page.get_by_text("不合格", exact=True).click()
        logged_in_page.get_by_label("备注").fill("UI测试用")
        logged_in_page.get_by_role("button", name="确 定").click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_unqualified_page(self, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
        logged_in_page.locator("li").filter(has_text="不合格产品报损").nth(1).click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_label("是否物流买赔").click()
        logged_in_page.get_by_title("否", exact=True).click()
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        logged_in_page.get_by_label("库区").click()
        logged_in_page.get_by_title("整件库区").click()
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.locator(".ag-selection-checkbox").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.locator("td:nth-child(11)").click()
        logged_in_page.get_by_role("cell", name="  不合格数量必须填写").get_by_role("textbox").fill("105")
        logged_in_page.locator("td:nth-child(12)").click()
        logged_in_page.get_by_role("cell", name=" 不合格原因必须填写").get_by_role("textbox").click()
        logged_in_page.get_by_text("超有效期").click()
        logged_in_page.locator("td:nth-child(15)").click()
        logged_in_page.get_by_role("cell", name=" 处理意见必须填写").get_by_role("textbox").click()
        logged_in_page.get_by_text("报损", exact=True).click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div > .ant-btn").first.click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
        logged_in_page.get_by_text("不合格产品报损", exact=True).first.click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator(".action_btn > div:nth-child(3) > .ant-btn").first.click()
        logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()

    def test_unqualified_destroy_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
        logged_in_page.locator("li").filter(has_text="不合格产品报损").nth(1).click()
        ncr_no = logged_in_page.locator(
            'xpath=//*[@id="app"]/section/section/section/div[3]/div/div/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div[1]').inner_text()
        print(ncr_no)
        audit_url = "http://192.168.111.232:17777/oms_232/api/erp/ncr/reBackNcr"
        audit_data = {
            "origCompanyCode": "ZHQC",
            "origWarehouseCode": "MRCK",
            "ncrNo": f"{ncr_no}",
            "origSys": "CQ_ERP",
            "replyUser": "李鸿宾",
            "replyDate": "2024-08-29 14:00:00",
            "replyDept": "个人事业部",
            "replyNotes": "全部同意",
            "dtList": [
                {
                    "rowNo": "1",
                    "agreeQty": 105,
                    "erpReportCode": "ERP-111111"
                }
            ]
        }
        audit_result = requests.post(url=audit_url, json=audit_data, headers=login_session).json()
        print(audit_result)
        if audit_result['msg'] == "成功":
            logged_in_page.locator("li").filter(has_text="GSP管理").click()
            logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
            logged_in_page.locator("li").filter(has_text="销毁作业").nth(1).click()
            logged_in_page.get_by_role("button", name="新 增").click()
            logged_in_page.get_by_label("货主").click()
            logged_in_page.get_by_title("智汇奇策科技有限公司").click()
            logged_in_page.get_by_label("分类标识").click()
            logged_in_page.get_by_title("药品").click()
            logged_in_page.get_by_label("销毁地点").click()
            logged_in_page.get_by_label("销毁地点").fill("山东省青岛市市北区")
            logged_in_page.get_by_role("button", name="添加明细").click()
            logged_in_page.get_by_label("通用名称").click()
            logged_in_page.get_by_label("通用名称").fill("氨糖")
            logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
            logged_in_page.get_by_role("button", name="查 询").click()
            logged_in_page.locator(".ag-selection-checkbox").first.click()
            logged_in_page.get_by_role("button", name="确 定").nth(1).click()
            logged_in_page.get_by_role("button", name="确 定").first.click()
            logged_in_page.get_by_role("button", name="查看").first.click()
            logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
            logged_in_page.locator("li").filter(has_text="销毁作业").nth(1).click()
            logged_in_page.get_by_role("button", name="编辑").first.click()
            logged_in_page.get_by_role("button", name="确 定").first.click()
            logged_in_page.get_by_role("button", name="一次审核").first.click()
            logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
            logged_in_page.get_by_role("button", name="二次审核").first.click()
            logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
            logged_in_page.locator("span").filter(has_text="李鸿宾").first.click()
            logged_in_page.get_by_role("menuitem", name="退出系统").locator("span").nth(1).click()
            logged_in_page.get_by_role("dialog").get_by_role("button", name="确 定").click()
            logged_in_page.get_by_placeholder("请输入账号").click()
            logged_in_page.get_by_placeholder("请输入账号").fill("lihongbin‘’")
            logged_in_page.get_by_placeholder("请输入账号").press("ArrowLeft")
            logged_in_page.get_by_placeholder("请输入账号").press("ArrowRight")
            logged_in_page.get_by_placeholder("请输入账号").fill("lihongbin")
            logged_in_page.get_by_placeholder("请输入密码").click()
            logged_in_page.get_by_placeholder("请输入密码").fill("lhx7758521")
            logged_in_page.locator("#warehouse").select_option("1")
            logged_in_page.get_by_role("button", name="登录").click()
            logged_in_page.locator("li").filter(has_text="GSP管理").click()
            logged_in_page.locator("div").filter(has_text=re.compile(r"^不合格管理$")).click()
            logged_in_page.locator("li").filter(has_text="销毁作业").nth(1).click()
            logged_in_page.get_by_role("button", name="二次审核").first.click()
            logged_in_page.get_by_role("button", name="确 定").click()
            expect(logged_in_page.get_by_role("grid")).to_contain_text("二次审核完成")
        else:
            print(f"erp审核失败: {audit_result}")

    def test_urge_sales_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP管理").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^滞销管理$")).click()
        logged_in_page.locator("li").filter(has_text="滞销催销").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="新 增").click()
        logged_in_page.get_by_label("货主").click()
        logged_in_page.get_by_title("智汇奇策科技有限公司").click()
        logged_in_page.get_by_label("分类标识").click()
        logged_in_page.get_by_title("药品").click()
        logged_in_page.get_by_label("备注").click()
        logged_in_page.get_by_label("备注").fill("UI测试用")
        logged_in_page.get_by_role("button", name="添加产品明细").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").click()
        logged_in_page.get_by_role("spinbutton", name="请输入").fill("10")
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.get_by_label("通用名称").click()
        logged_in_page.get_by_label("通用名称").fill("氨糖")
        logged_in_page.get_by_title("氨糖--50g--智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="查 询").click()
        time.sleep(1)
        logged_in_page.get_by_role("row", name=" 1", exact=True).locator("div").first.click()
        logged_in_page.get_by_role("button", name="确 定").nth(1).click()
        logged_in_page.get_by_role("button", name="确 定").first.click()
        logged_in_page.locator("li").filter(has_text="产品滞销预警").nth(1).click()
        logged_in_page.get_by_role("button", name="搜索").click()
        logged_in_page.locator(".zhqc-layout-content > div > section").click()
        logged_in_page.locator("#app").get_by_placeholder("请输入").fill("10")
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_gsp_resave_record_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品收货记录").nth(1).click()
        logged_in_page.get_by_role("button", name="新增条件").click()
        logged_in_page.locator("div:nth-child(5) > .flex > .ant-select > .ant-select-selector").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^通用名称$")).nth(1).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_8").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品收货记录")).to_contain_text("氨糖")

    def test_gsp_check_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品验收记录").nth(1).click()
        logged_in_page.locator("form").get_by_text("批号").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^通用名称$")).nth(2).click()
        logged_in_page.locator(".ant-select-selection-overflow").click()
        logged_in_page.locator("#rc_select_7").fill("氨糖")
        logged_in_page.get_by_title("氨糖---50g---智汇奇策科技有限公司").click()
        logged_in_page.locator("td:nth-child(11) > .vxe-cell").first.click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品验收记录")).to_contain_text("氨糖")

    def test_gsp_in_order_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品入库记录").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").nth(1).fill("20240910001")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品入库记录")).to_contain_text("M12321321")

    def test_gsp_out_order_fh_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品出库复核记录").nth(1).click()
        logged_in_page.get_by_placeholder("请输入").click()
        logged_in_page.get_by_placeholder("请输入").fill("20240910001")
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品出库复核记录")).to_contain_text("批发销售单")

    def test_gsp_yh_check_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品养护确认记录").nth(1).click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.get_by_title("重点养护").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.locator("td:nth-child(6) > .vxe-cell > .vxe-cell--label").first).to_be_visible()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_gsp_th_record_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品养护记录").nth(1).click()
        logged_in_page.locator("#rc_select_6").click()
        logged_in_page.get_by_title("重点养护").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品养护记录")).to_contain_text("金嗓子喉宝")
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()

    def test_gsp_recheck_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="产品复检记录").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("药品质量复检记录")).to_contain_text("氨糖")

    def test_gsp_unqualify_record_page(self, login_session, logged_in_page: Page) -> None:
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.reload()
        logged_in_page.locator("li").filter(has_text="首页").click()
        logged_in_page.locator("li").filter(has_text="GSP记录").click()
        logged_in_page.locator("div").filter(has_text=re.compile(r"^GSP记录$")).click()
        logged_in_page.locator("li").filter(has_text="不合格产品报损记录").nth(1).click()
        logged_in_page.get_by_role("button", name="重置").click()
        logged_in_page.get_by_role("button", name="搜索").click()
        expect(logged_in_page.get_by_label("不合格药品报损记录")).to_contain_text("超有效期")
