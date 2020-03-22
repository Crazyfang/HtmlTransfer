from bs4 import BeautifulSoup, element
import re
import sys
import logging
import time
import os
import Surface
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal


def generate_logging():
    """
    return:
        The logger output the log message

    """
    # First, generate a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Second, generate a log handler to write the log file
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.getcwd() + '/Logs/'
    if os.path.exists(log_path):
        pass
    else:
        os.mkdir(log_path)

    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)

    # Third, define the output format of handler
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)

    # Four, add the handler into logger
    logger.addHandler(fh)

    return logger


class DataTransactionFlow:
    """
    this is the data class to get the external data
    Attributes:
        name:户名
        account_number:账号
        transaction_code:交易码
        debtor_sum:借方发生额
        creditor_sum:贷方发生额
        balance:余额
        operator:操作员
        digest:摘要
    """
    def __init__(self,
                 name,
                 account_number,
                 date,
                 transaction_code,
                 debtor_sum,
                 creditor_sum,
                 balance,
                 operator,
                 digest):
        self.name = name
        self.account_number = account_number
        self.date = date
        self.transaction_code = transaction_code
        self.debtor_sum = debtor_sum
        self.creditor_sum = creditor_sum
        self.balance = balance
        self.operator = operator
        self.digest = digest


# TODO(fangyonglubu@qq.com):Get data from list_string and transform them into data class,
#  finally insert into table of database
# TODO(fangyonglubu@qq.com):2020-3-22 0:06 complete the rest of GUI logic and insert data into the simulation database
class TransferClass:
    """
    the class use to get base html string from file and then transform them
    Attributes:None
    """
    def __init__(self, file_path='C:\\Users\\Administrator\\Desktop\\920103_sav_full.htm'):
        self.file_path = file_path
        self.table_assemble = element.ResultSet(None)
        self.bill_length = 0
        self.logger = generate_logging()

    def read_data(self):
        """
        Read data from html file and print them, just the function demo and verify the technical feasibility
        Args:None
        Returns:None
        """
        # open file and read data
        html_file = open(self.file_path, 'r')
        html_handler = html_file.read()

        # get the bs handler
        # the features can change to other resolver including html.parser, lxml, xml or lxml-xml, html5lib
        soup = BeautifulSoup(html_handler, features='lxml')

        self.table_assemble = soup.find_all('table')
        # list_string = []

        # get the table node from the all html string
        # for index, table in enumerate(soup.find_all('table')):
        #     if index == 1:
        #         for index1, pre in enumerate(table.find_all('pre')):
        #             string = pre.string
        #             if string:
        #                 # wipe out the blank as far as possible
        #                 list_string.append(' '.join(string.split()))

        # pattern = re.compile(r'[0-9]{4}/[0-9]{2}/[0-9]{2}')
        # pattern = re.compile(r'^[\u4e00-\u9fa5]{2}.{2}(\d+).')
        # pattern = re.compile(r'帐号：\[(\d+)\]')
        # pattern = re.compile(r'户名：\[\s*([\u4e00-\u9fa5]+)\s*\]')
        # for i in list_string:
        #     match = pattern.findall(i)
        #     if match:
        #         print(match)
        #     print(i)

        # table_bs = BeautifulSoup(table, features='lxml')
        # if index == 1:
        #     print(table.find_all('pre')

        # print(soup.find_all('pre'))

    def process_data(self, index):
        list_string = []
        for item in self.table_assemble[index].find_all('pre'):
            string = item.string
            if string:
                list_string.append(' '.join(string.split()))

        # regular pattern
        pattern_number = re.compile(r'帐号：\[(\d+)\]')
        pattern_name = re.compile(r'户名：\[\s*([\u4e00-\u9fa5]+\s*[\u4e00-\u9fa5]+)\s*\]')
        pattern_detail = re.compile(r'[0-9]{4}/[0-9]{2}/[0-9]{2}')

        # temporary variable
        sign_dont_repeat = False
        name = ''
        account_number = ''
        count = 0

        for item in list_string:
            match_number = pattern_number.findall(item)
            if match_number:
                account_number = match_number[0]
                name = pattern_name.findall(item)[0]
                sign_dont_repeat = True
                continue

            if sign_dont_repeat:
                if pattern_detail.findall(item):
                    transaction_flow = DataTransactionFlow(name, account_number, *item.split())
                    count += 1
                    # insert database

        self.logger.info('账号:{0},户名:{1},流水条数:{2} 插入成功!'.format(account_number, name, count))

        return [True, account_number, name, count]

        # pass

    def return_bill_length(self):
        if self.bill_length:
            return self.bill_length
        else:
            self.bill_length = len(self.table_assemble)
            return self.bill_length


class ThreadTransfer(QThread):
    signOut = pyqtSignal(str, float)

    def __init__(self, file_path):
        super(ThreadTransfer, self).__init__()
        self.file_path = file_path

    def run(self):
        transfer = TransferClass(self.file_path)

        transfer.read_data()

        bill_length = transfer.return_bill_length()
        self.signOut.emit('当前账页共读取{0}行', 0)
        for index in range(bill_length):
            return_data = transfer.process_data(index)
            if return_data[0]:
                self.signOut.emit('账页账号:{0}, 户名:{1}, 账页信息条数:{2}'.format(return_data[1], return_data[2], return_data[3]),
                                  (index + 1) / bill_length * 100)
            else:
                self.signOut.emit('当前账页处理出现错误，请查看日志文件输出!')

        # self.signOut.emit('当前文件账页读取完毕!', 100)


class FunctionPage(QMainWindow, Surface.Ui_MainWindow):
    def __init__(self):
        # 消除警告
        # noinspection PyArgumentList
        QMainWindow.__init__(self)
        Surface.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.message = []
        self.slm = QStringListModel()

        self.work_thread = None
        self.step = 0  # 进度条的值
        self.progressBar_Progress.setValue(0)
        self.Button_SelectFile.clicked.connect(self.select_file)
        self.Button_Start.clicked.connect(self.start_process)

    def select_file(self):
        # noinspection PyArgumentList
        filename_choose, file_type = QFileDialog.getOpenFileName(None, '打开', r'./', 'Html Files (*.htm);;All Files (*)')
        self.lineEdit_SelectFile.setText(filename_choose)

    def start_process(self):
        if not self.lineEdit_SelectFile.text():
            # noinspection PyArgumentList
            QMessageBox.information(None, '提示', '请选择HTML文件!')
        else:
            pass
        self.work_thread = ThreadTransfer(self.lineEdit_SelectFile.text())

        self.work_thread.signOut.connect(self.list_add)
        self.Button_Start.setEnabled(False)
        self.Button_Start.setText('正在处理')
        self.work_thread.start()

    def set_progress_bar(self):
        self.step += 1
        self.progressBar_Progress.setValue(self.step)

    def list_add(self, message, state):
        self.message.append(message)
        self.slm.setStringList(self.message)
        self.listView_Info.setModel(self.slm)
        self.listView_Info.scrollToBottom()
        self.progressBar_Progress.setValue(state)
        if state >= 100:
            self.Button_Start.setEnabled(True)
            self.Button_Start.setText('开始处理')
            # noinspection PyArgumentList
            QMessageBox.information(None, "提示", "程序处理完成")


if __name__ == '__main__':
    # instance = TransferClass()
    # instance.read_data()
    # i = instance.return_bill_length()
    # for index in range(i):
    #     instance.process_data(index)
    # print('账号：'.encode('utf8'))
    # string = '帐号：[920103010110001009]   户名：[    刘成福]'
    #
    # print(string.split())
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = FunctionPage()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
