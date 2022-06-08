import requests
from rich.table import Table
from rich.progress import Progress

progress = Progress()


class shodan:

    def __init__(self, apikey):
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        self.table = Table()
        progress.console.rule('[green][INFO] 正在shodan上查询 %s 的信息...' % ip)
        self.url = "https://api.shodan.io/shodan/host/{}?key={}".format(ip, self.apikey)
        try:
            self.data = requests.get(self.url, timeout=timeout).json()
        except BaseException as e:
            progress.console.print("[red][WRONG] shodan查询失败！IP格式错误或请求超时! 错误信息为: %s " % e)
            return None

        if 'error' in self.data:
            progress.console.print('[yellow][WARNING] 没有在shodan上查询到 %s 的相关信息' % ip)
            return None
        else:
            try:
                target_ip = self.data['ip_str']
            except TypeError:
                target_ip = "N/A"

            try:
                target_port = ""
                for item in self.data['ports']:
                    target_port += str(item) + "、"
            except BaseException as e:
                progress.console.log(e)
                target_port = ""

            try:
                target_hostname = ""
                for item in self.data['hostnames']:
                    target_hostname += item + "、"
            except TypeError:
                target_hostname = ""

            try:
                target_domain = ""
                for item in self.data['domains']:
                    target_domain += item + "、"
            except TypeError:
                target_domain = ""

            try:
                target_isp = self.data['isp']
            except TypeError:
                target_isp = "N/A"

            self.table.add_column("IP", justify="center")
            self.table.add_column("开放的端口", justify="left")
            self.table.add_column("域名", justify="left")
            self.table.add_column("子域名", justify="left")
            self.table.add_column("运营商", justify="left")

            self.table.add_row(target_ip, target_port[:-1], target_domain, target_hostname[:-1], target_isp)

            return self.table

    def get_domain(self):
        try:
            return self.table.columns[3]._cells[0].split("、")
        except BaseException:
            return []