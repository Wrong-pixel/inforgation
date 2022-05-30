import requests
from rich.console import Console
from rich.table import Table

console = Console()


class zoomeye:

    def __init__(self, apikey):
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        table = Table()
        console.rule('[green][INFO] 正在zoomeye上查询 %s 的信息...' % ip)
        url = "https://api.zoomeye.org/host/search?query=%s" % ip
        headers = {
            "API-KEY": self.apikey
        }
        data = requests.request("GET", url=url, headers=headers, timeout=timeout).json()
        if data['total'] != 0:
            table.add_column("IP", justify="left")
            table.add_column("应用", justify="left")
            table.add_column("端口", justify="left")
            table.add_column("服务", justify="left")
            table.add_column("服务标题", justify="left")
            for item in data['matches']:
                try:
                    target_ip = item['ip']
                    target_hostname = item['portinfo']['app']
                    target_port = str(item['portinfo']['port'])
                    target_service = item['portinfo']['service']
                    target_title = item['portinfo']['title'][0] if item['portinfo']['title'][0] else ""
                except BaseException:
                    pass
                table.add_row(target_ip, target_hostname, target_port, target_service, target_title)
            return table
        else:
            console.print('[yellow][WARNING] 没有在zoomeye上查询到 %s 的相关信息' % ip)
            return None