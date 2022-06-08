import requests
from rich.progress import Progress
from rich.table import Table

progress = Progress()


class zoomeye:

    def __init__(self, apikey):
        self.apikey = apikey

    def get_result(self, ip, timeout=10):
        self.table = Table()
        progress.console.rule('[green][INFO] 正在zoomeye上查询 %s 的信息...' % ip)
        url = "https://api.zoomeye.org/host/search?query=%s" % ip
        headers = {
            "API-KEY": self.apikey
        }
        try:
            data = requests.request("GET", url=url, headers=headers, timeout=timeout).json()
        except BaseException as e:
            progress.console.print("[red][WRONG] 查询zoomeye信息超时！")
            return None
        if data['total'] != 0:
            self.table.add_column("IP", justify="left")
            self.table.add_column("应用", justify="left")
            self.table.add_column("端口", justify="left")
            self.table.add_column("服务", justify="left")
            self.table.add_column("服务标题", justify="left")
            for item in data['matches']:
                target_ip = item['ip']
                target_hostname = item['portinfo']['app'] if item['portinfo']['app'] else ""
                target_port = str(item['portinfo']['port']) if item['portinfo']['port'] else ""
                target_service = item['portinfo']['service'] if item['portinfo']['service'] else ""
                target_title = item['portinfo']['title'][0] if item['portinfo']['title'] is not None else ""
                self.table.add_row(target_ip, target_hostname, target_port, target_service, target_title)
            return self.table
        else:
            progress.console.print('[yellow][WARNING] 没有在zoomeye上查询到 %s 的相关信息' % ip)
            return None
