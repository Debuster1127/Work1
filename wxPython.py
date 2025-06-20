import wx
import psycopg2

def get_connection():
        return psycopg2.connect(
            database="postgres",
            user="postgres",
            password="TW3VJywpTx",
            host="localhost",
            port="5489",
        )

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title= "Окно входа")
        panel = wx.Panel(self)

        login_label = wx.StaticText(panel, label = "Логин")
        self.login_input = wx.TextCtrl(panel)

        pass_label = wx.StaticText(panel, label = "Пароль")
        self.pass_input = wx.TextCtrl(panel, style=wx.TE_PASSWORD)

        login_button = wx.Button(panel, label = "Вход")
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(login_label, 0, wx.ALL, 10)
        sizer.Add(self.login_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(pass_label, 0, wx.ALL, 10)
        sizer.Add(self.pass_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(login_button, 0, wx.ALIGN_CENTER, 15)

        panel.SetSizer(sizer)
        self.SetSize((300,200))
        self.Show()

    def on_login(self, event):
        login = self.login_input.GetValue()
        password= self.pass_input.GetValue()

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT username, userrole FROM "User" WHERE userlogin=%s AND userpassword=%s',
                (login, password)
            )

            result = cursor.fetchone()

            print(result)

            if result:
                username, userrole = result
                wx.MessageBox(f"Добро пожаловать, {username}", "Успешный вход")

                if userrole == 1:
                    self.open_admin_window
                elif userrole == 2:
                    self.open_manager_window
                elif userrole == 3:
                    self.open_client_window

                self.Close()
            else:
                wx.MessageBox("Неверный логин или пароль", "Ошибка", wx.ICON_ERROR)

            cursor.close()
            conn.close()

        except Exception as e:
            wx.MassageBox("Ошибка подключения: \n{e}", "Ошибка", wx.ICON_ERROR)


if __name__ == '__main__':
    app = wx.App(False)
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()