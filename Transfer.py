from bs4 import BeautifulSoup
import re


# TODO(fangyonglubu@qq.com):Get data from list_string and transform them into data class,
#  finally insert into table of database
class TransferClass:
    """
    the class use to get base html string from file and then transform them
    Attributes:None
    """
    url = 'C:\\Users\\Administrator\\Desktop\\920103_sav_full.htm'

    def read_data(self):
        """
        Read data from html file and print them, just the function demo and verify the technical feasibility
        Args:None
        Returns:None
        """
        # open file and read data
        html_file = open(self.url, 'r')
        html_handler = html_file.read()

        # get the bs handler
        # the features can change to other resolver including html.parser, lxml, xml or lxml-xml, html5lib
        soup = BeautifulSoup(html_handler, features='lxml')
        list_string = []

        # get the table node from the all html string
        for index, table in enumerate(soup.find_all('table')):
            if index == 1:
                for index1, pre in enumerate(table.find_all('pre')):
                    string = pre.string
                    if string:
                        # wipe out the blank as far as possible
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
