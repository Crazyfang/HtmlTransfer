from bs4 import BeautifulSoup
import re


class TransferClass:
    url = 'C:\\Users\\Administrator\\Desktop\\920103_sav_full.htm'

    def read_data(self):
        html_file = open(self.url, 'r')
        html_handler = html_file.read()

        soup = BeautifulSoup(html_handler, features='lxml')
        list_string = []

        for index, table in enumerate(soup.find_all('table')):
            if index == 1:
                for index1, pre in enumerate(table.find_all('pre')):
                    string = pre.string
                    if string:
                        list_string.append(' '.join(string.split()))

        # pattern = re.compile(r'[0-9]{4}/[0-9]{2}/[0-9]{2}')
        # pattern = re.compile(r'^[\u4e00-\u9fa5]{2}.{2}(\d+).')
        # pattern = re.compile(r'帐号：\[(\d+)\]')
        pattern = re.compile(r'户名：\[\s*([\u4e00-\u9fa5]+)\s*\]')
        for i in list_string:
            match = pattern.findall(i)
            if match:
                print(match)
            print(i)

        # table_bs = BeautifulSoup(table, features='lxml')
        # if index == 1:
        #     print(table.find_all('pre')

        # print(soup.find_all('pre'))


if __name__ == '__main__':
    instance = TransferClass()
    instance.read_data()
    # print('账号：'.encode('utf8'))
    # string = '帐号：[920103010110001009]   户名：[    刘成福]'
    #
    # print(string.split())
