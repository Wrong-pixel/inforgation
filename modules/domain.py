from rich.table import Table
from rich.console import Console

console = Console()


class domain:

    def __init__(self, domain_list: list):
        self.domain_list = domain_list

    def get_result(self):
        # 如果不是空的，把多余的"N/A"除掉，实例化时已经对域名列表去重了，这里就不需要再去，但是考虑到列表的remove方法，得加一个try
        # 先试着把N/A去掉，不确定是不是列表里面只有一个N/A
        try:
            self.domain_list.remove("N/A")
        # 列表里面没有N/A这个元素，会报错，处理一下
        except ValueError:
            pass
        # 实例化的列表=可能是空的，表示没有域名信息，直接返回None，主函数就不会将空table传入output列表
        if not self.domain_list:
            return None
        # 打个横幅
        console.rule('[green][INFO]域名结果汇总')
        # 实例化一个空table
        table = Table()
        # 列标题
        table.add_column("IP绑定的域名")
        for item in self.domain_list:
            # 添加列元素
            table.add_row(item)
        return table