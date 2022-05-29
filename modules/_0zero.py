from rich.console import Console
from rich.table import Table
import requests

console = Console()


class _0zero:

    def __init__(self, apikey):
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        console.rule('[green][INFO] 正在0zero上查询 %s 的威胁情报...' % ip)
        self.table = Table()
        self.table.add_column("IP", justify="left")
        self.table.add_column("端口", justify="left")
        self.table.add_column("url", justify="left")
        self.table.add_column("网页标题", justify="center")
        self.table.add_column("操作系统", justify="center")
        self.table.add_column("服务器", justify="center")
        self.table.add_column("运营商", justify="center")
        self.table.add_column("协议", justify="center")
        url = "https://0.zone/api/data/"
        query = {
            "title": "ip={}".format(ip),
            "title_type": "site",
            "page": 1,
            "pagesize": 10,
            "zone_key_id": "{}".format(self.apikey)
        }
        try:
            text = requests.request("POST", url, data=query, timeout=timeout).json()
        except requests.ReadTimeout:
            console.print("[red][WRONG] 查询0zero信息超时")
            return None
        if text['code'] == 1:
            console.print("[red][WRONG] 查询出错，错误信息为: %s " % (text['message']))
            return None
        if not text['data']:
            console.print("[yellow][WARNING] 没有在0zero平台查询到相关信息!")
            return None
        for item in text['data']:
            target_ip = item["ip"] if item["ip"] else "N/A"
            target_port = item["port"] if item["port"] else "N/A"
            target_url = item["url"] if item["url"] else "N/A"
            target_title = item["title"] if item["title"] else "N/A"
            target_os = item["os"] if item["os"] else "N/A"
            target_component = item["component"] if item["component"] else "N/A"
            target_operator = item["operator"] if item["operator"] else "N/A"
            target_protocol = item["protocol"] if item["protocol"] else "N/A"
            self.table.add_row(target_ip, target_port, target_url, target_title, target_os, target_component,
                               target_operator, target_protocol)
        return self.table
