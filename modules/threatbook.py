import requests
from rich.table import Table
from rich.progress import Progress

progress = Progress()


class threatbook:
    def __init__(self, apikey):
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        self.table = Table()
        progress.console.rule('[green][INFO] 正在微步上查询 %s 的威胁情报...' % ip)
        self.url = "https://api.threatbook.cn/v3/scene/ip_reputation"
        query = {
            "apikey": self.apikey,
            "resource": ip,
            "lang": "zh"
        }
        try:
            self.data = requests.request("GET", self.url, params=query, timeout=timeout).json()
        except requests.ReadTimeout:
            progress.console.print("[red][WRONG] 查询微步信息超时")
            return None
        if self.data['response_code']:
            progress.console.print(
                "[red][WRONG]微步查询失败！错误码：%s ，错误信息: %s " % (self.data['response_code'], self.data['verbose_msg']))
            return None
        self.data = self.data['data'][ip]
        self.table.add_column("威胁等级", justify="center")
        self.table.add_column("IP类型判断", justify="center")
        self.table.add_column("威胁类型", justify="center")
        self.table.add_column("运营商", justify="center")
        self.table.add_column("地理位置", justify="center")
        self.table.add_column("场景", justify="center")
        self.table.add_column("情报可信度", justify="center")
        target_severity = self.data['severity']
        target_judgments = ""
        for item in self.data['judgments']:
            target_judgments += item + ","
        target_tags = ""
        for item in self.data['tags_classes']:
            for tag in item['tags']:
                target_tags += tag
        target_carrier = self.data['basic']['carrier']
        target_location = self.data['basic']['location']['country'] + " " + self.data['basic']['location']['province'] + self.data['basic']['location']['city']
        target_scene = self.data['scene']
        target_confidence_level = self.data['confidence_level']
        self.table.add_row(target_severity, target_judgments[:-1], target_tags, target_carrier, target_location,
                           target_scene, target_confidence_level)
        return self.table

    def get_domain(self):
        return self.table
