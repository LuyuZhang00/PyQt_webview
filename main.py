import psycopg2
from PyQt5.QtCore import QPoint

from LoginUI import *
from InterfaceUI import *
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

user_now = ""
class MoveWindow(QMainWindow):
    """
    重写鼠标事件，实现窗口拖动
    """
    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
    def mousePressEvent(self, event):
        """
        鼠标点击事件
        :param event:
        :return:
        """
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):

        """
        鼠标移动事件
        :param event:
        :return:
        """
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

# class LoginWindow(QMainWindow):
class LoginWindow(MoveWindow):
    """
    登录界面
    """
    def __init__(self):
        """
        初始化
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)               # 调用Ui_MainWindow类中的setupUi方法，创建界面
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)    # 设置窗口无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)  # 设置窗口阴影
        self.shadow.setOffset(5, 5)       # 设置阴影偏移
        self.shadow.setBlurRadius(10)   # 设置阴影半径
        self.shadow.setColor(QtCore.Qt.black)  # 设置阴影颜色
        self.ui.frame.setGraphicsEffect(self.shadow)  # 在frame上添加阴影
        # self.oldPos = self.pos()

        self.ui.pushButton_login.clicked.connect(lambda :self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_register.clicked.connect(self.pushButton_registerview)
        self.ui.pushButton_l_sure.clicked.connect(self.login_in)
        self.ui.pushButton_d_sure.clicked.connect(self.register_in)

        self.show()

    def pushButton_registerview(self):
        """
        注册界面
        :return:
        """
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.ui.stackedWidget.setCurrentIndex(0)

    def login_in(self):
        """
        登录
        :return:
        """
        account = self.ui.lineEdit_l_account.text()
        password = self.ui.lineEdit_l_passward.text()
        print(account, password)
        # 数据库连接
        account_list = []
        password_list = []
        conn =psycopg2.connect(database="DataMy",user="postgres",password="123456",host="localhost",port="5432")
        cur = conn.cursor()
        cur.execute("select * from users")
        rows=cur.fetchall()
        for row in rows:
            account_list.append(row[0])
            password_list.append(row[1])
        print(account_list, password_list)
        conn.commit()
        cur.close()

        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)

            elif account == account_list[i] and password == password_list[i]:
                global user_now
                user_now = account
                self.w=MyWindow()
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)
    def register_in(self):
        """
        注册
        :return:
        """
        account = self.ui.lineEdit_d_account.text()
        password = self.ui.lineEdit_d_passward.text()
        password_sure = self.ui.lineEdit_d_rpassward.text()
        if len(account)==0 or len(password)==0 or len(password_sure)==0:
            self.ui.stackedWidget.setCurrentIndex(1)
        elif password != password_sure:
            self.ui.stackedWidget.setCurrentIndex(4)
        else:
            conn = psycopg2.connect(database="DataMy", user="postgres", password="123456", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute(f"insert into users values('{account}','{password}')")
            conn.commit()
            cur.close()
            self.ui.stackedWidget_2.setCurrentIndex(3)
            print("修改成功")



    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     delta = QPoint(event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()

# class MyWindow(QMainWindow):
class MyWindow(MoveWindow):
    """
    主界面
    """
    def __init__(self):
        """
        初始化
        """
        super().__init__()
        self.ui = Ui_MyWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(5, 5)
        self.shadow.setBlurRadius(20)
        # self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame_6.setGraphicsEffect(self.shadow)

        self.ui.pushButton_home.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_web.clicked.connect(self.gp_web)
        self.ui.pushButton_my.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_logout.clicked.connect(self.log_out)
        self.ui.pushButton_4.clicked.connect(self.change_password)
        self.show()
    def gp_web(self):
        """
        网页浏览
        :return:
        """
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton_bilibili.clicked.connect(lambda :webbrowser.open("https://www.bilibili.com/"))
        self.ui.pushButton_csdn.clicked.connect(lambda :webbrowser.open("https://blog.csdn.net/"))
        self.ui.pushButton_vedio.clicked.connect(lambda :webbrowser.open("https://www.iqiyi.com/"))
        self.ui.pushButton_apple.clicked.connect(lambda :webbrowser.open("https://www.apple.com/cn/"))

    def log_out(self):
        """
        退出登录
        :return:
        """
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ""

    def change_password(self):
        """"
        修改密码
        :return:
        """
        global user_now
        password=self.ui.lineEdit_m_pass.text()
        if len(self.ui.lineEdit_m_pass.text()) == 0 or len(self.ui.lineEdit_m_pass_sure.text()) == 0:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        elif self.ui.lineEdit_m_pass.text() != self.ui.lineEdit_m_pass_sure.text():
            self.ui.stackedWidget_2.setCurrentIndex(2)
        elif self.ui.lineEdit_m_pass.text() == self.ui.lineEdit_m_pass_sure.text():
            conn = psycopg2.connect(database="DataMy", user="postgres", password="123456", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute(f"update users set passwords = '{password}' where accounts = '{user_now}'")
            conn.commit()
            cur.close()
            self.ui.stackedWidget_2.setCurrentIndex(3)
            print("修改成功")

if __name__ == "__main__":
    """
    主函数
    
    """
    app = QApplication(sys.argv)
    w = LoginWindow()
    # w = MyWindow()
    sys.exit(app.exec_())
