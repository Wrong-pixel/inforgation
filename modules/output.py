import jinja2
import pandas as pd
import time

import rich.table


class output:

    def __init__(self, ip, file_name, table_list):
        # 报告中的IP字段
        self.ip = ip
        # 报告名
        self.file_name = file_name
        # 报告中用来生成表格的table列表，单个元素为字典，字典键为平台名，值为rich.table.Table
        self.table_list = table_list

    def output_html(self):
        # 创建jinjia2渲染模版
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
        template = env.get_template('./modules/Template.html')

        # 报告中的时间
        check_time = time.strftime('%Y-%m-%d-%H:%M:%S')
        # 创建一个空列表存放最终传给模版渲染的表格内容
        tables = []
        # 首先遍历传入的列表
        for item in self.table_list:
            # 列表中的单个元素为字典类型，k表示取平台名，v表示取table对象
            for k, v in item.items():
                # 将tables对象转化为html语言后重新生成一个字典并放入tables列表
                tables.append({k: self.get_html(v)})
        html = template.render(times=check_time, tables=tables, IP=self.ip)
        with open("./output/{}.html".format(self.file_name), "w", encoding='utf-8') as f:
            f.write(html)
        f.close()

    # 此方法将table对象转化为html语言
    def get_html(self, table: rich.table.Table):
        # 为什么是字典，因为rich.table.Table的取值是按列来去的，分为列名(header属性)以及属性值列表(_cells属性)，获取这两个内容才能通过pandas生成表格
        table_data = {}
        # 按列，转化为字典
        for item in table.columns:
            table_data.update({item.header: item._cells})
        # pandas生成html语言，返回，注意每次调用只返回一个table的html语言，
        # 在上面的output方法中传入模版的是需要一个列表，列表的单个元素是字典，字典键为表格名（即平台名），字典值为对应表格的html代码
        return pd.DataFrame(table_data, ).to_html(justify="left", index=False, na_rep="N/A")
