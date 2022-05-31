import requests
from base64 import b64encode
from rich.table import Table
from rich.console import Console

console = Console()


class hunter:

    def __init__(self, username, apikey):
        self.username = username
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        self.table = Table()
        console.rule('[green][INFO] 正在鹰图上查询 %s 的信息...' % ip)
        # base64加密查询语句
        words = b64encode(bytes('ip="{}"'.format(ip).encode())).decode()
        # 拼接url
        self.url = "https://hunter.qianxin.com/openApi/search?username={}&api-key={}&search={}&page=1&page_size=10&is_web=1".format(
            self.username, self.apikey, words)
        # 解析json数据
        try:
            # 超时处理，默认为5秒
            self.data = requests.get(self.url, timeout=timeout).json()
        except BaseException as e:
            console.print("[red][WRONG] 查询鹰图信息超时")
            return None
        if self.data['code'] != 200:
            console.print("[red][WRONG] 查询鹰图信息失败！%s " % (self.data['message']))
            return None
        # 消耗积分
        console.print("[green][INFO] "+self.data['data']['consume_quota'])
        # 剩余积分
        console.print("[green][INFO] "+self.data['data']['rest_quota'])
        # 创建输出表
        self.table.add_column('url', justify="left")
        self.table.add_column('端口', justify="left")
        self.table.add_column('网页标题', justify="left")
        self.table.add_column('域名', justify="left")
        self.table.add_column('状态码', justify="center")
        self.table.add_column('操作系统', justify="center")
        self.table.add_column('归属地', justify="center")
        self.table.add_column('运营商', justify="center")
        try:
            for data in self.data['data']['arr']:
                # 获取url
                target_url = data['url']
                # 获取端口
                target_port = str(data['port'])
                # 获取网页标题
                target_web_title = str(data['web_title']) if data['web_title'] else "N/A"
                # 获取域名
                target_domain = data['domain'] if data['domain'] else "N/A"
                # 获取状态码
                target_status_code = str(data['status_code'])
                # 获取操作系统
                target_os = data['os'] if data['os'] else "N/A"
                # 获取地理位置
                target_localtion = data['country'] + data['province'] + data['city']
                # 获取运营商
                target_isp = data['isp']
                # 添加到表格中
                self.table.add_row(target_url, target_port, target_web_title, target_domain, target_status_code,
                                   target_os, target_localtion, target_isp)
            return self.table
        except TypeError:
            # 可能是没查到结果，也可能是查询速度过快
            console.print('[yellow][WARNING] 没有在鹰图上查询到 %s 的相关信息' % ip)
            return None
        # 返回table对象

    def get_domain(self):
        try:
            return self.table.columns[3]._cells
        except BaseException as e:
            return []