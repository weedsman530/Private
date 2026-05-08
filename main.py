from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import datetime
import threading

try:
    from zk import ZK
except Exception:
    ZK = None

KV = r'''
<MainScreen>:
    orientation: "vertical"
    padding: dp(18)
    spacing: dp(12)

    Label:
        text: "ZKTeco Date/Time Tool"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: dp(44)

    Label:
        text: "غيّر وقت وتاريخ جهاز البصمة من الموبايل على نفس الواي فاي"
        font_size: "15sp"
        size_hint_y: None
        height: dp(44)
        text_size: self.width, None
        halign: "center"

    TextInput:
        id: ip_input
        text: root.device_ip
        hint_text: "Device IP"
        multiline: False
        input_filter: None
        font_size: "18sp"
        size_hint_y: None
        height: dp(52)

    TextInput:
        id: port_input
        text: root.device_port
        hint_text: "Port"
        multiline: False
        input_filter: "int"
        font_size: "18sp"
        size_hint_y: None
        height: dp(52)

    BoxLayout:
        orientation: "horizontal"
        spacing: dp(10)
        size_hint_y: None
        height: dp(52)
        Button:
            text: "Connect"
            disabled: root.busy
            on_release: root.connect_device()
        Button:
            text: "Use Now"
            disabled: root.busy
            on_release: root.fill_now()

    TextInput:
        id: date_input
        text: root.date_text
        hint_text: "YYYY-MM-DD"
        multiline: False
        font_size: "18sp"
        size_hint_y: None
        height: dp(52)

    TextInput:
        id: time_input
        text: root.time_text
        hint_text: "HH:MM:SS"
        multiline: False
        font_size: "18sp"
        size_hint_y: None
        height: dp(52)

    Button:
        text: "Set Device Date/Time"
        size_hint_y: None
        height: dp(58)
        disabled: root.busy
        on_release: root.set_device_datetime()

    Button:
        text: "Sync Device With Mobile Current Time"
        size_hint_y: None
        height: dp(58)
        disabled: root.busy
        on_release: root.sync_now_to_device()

    Label:
        text: root.status
        font_size: "16sp"
        text_size: self.width, None
        halign: "center"
        valign: "middle"
'''

class MainScreen(BoxLayout):
    device_ip = StringProperty("192.168.1.201")
    device_port = StringProperty("4370")
    date_text = StringProperty("")
    time_text = StringProperty("")
    status = StringProperty("Ready")
    busy = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = None
        self.fill_now()

    def fill_now(self):
        now = datetime.datetime.now()
        self.date_text = now.strftime("%Y-%m-%d")
        self.time_text = now.strftime("%H:%M:%S")
        self.status = "تم وضع وقت الموبايل الحالي في الخانات"

    def _run_bg(self, fn):
        if self.busy:
            return
        self.busy = True
        threading.Thread(target=fn, daemon=True).start()

    def _finish(self, message):
        def update(_dt):
            self.status = message
            self.busy = False
        Clock.schedule_once(update, 0)

    def _get_ip_port(self):
        ip = self.ids.ip_input.text.strip()
        port_text = self.ids.port_input.text.strip() or "4370"
        return ip, int(port_text)

    def connect_device(self):
        def work():
            if ZK is None:
                self._finish("مكتبة pyzk غير موجودة داخل التطبيق. راجع خطوات البناء.")
                return
            try:
                ip, port = self._get_ip_port()
                zk = ZK(ip, port=port, timeout=8, password=0, force_udp=False, ommit_ping=False)
                self.conn = zk.connect()
                self._finish("تم الاتصال بجهاز البصمة بنجاح")
            except Exception as e:
                self.conn = None
                self._finish(f"فشل الاتصال: {e}")
        self.status = "جاري الاتصال..."
        self._run_bg(work)

    def _ensure_conn(self):
        if self.conn:
            return self.conn
        ip, port = self._get_ip_port()
        zk = ZK(ip, port=port, timeout=8, password=0, force_udp=False, ommit_ping=False)
        self.conn = zk.connect()
        return self.conn

    def set_device_datetime(self):
        def work():
            if ZK is None:
                self._finish("مكتبة pyzk غير موجودة داخل التطبيق. راجع خطوات البناء.")
                return
            try:
                dt = datetime.datetime.strptime(
                    self.ids.date_input.text.strip() + " " + self.ids.time_input.text.strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception:
                self._finish("صيغة التاريخ أو الوقت غلط. استخدم YYYY-MM-DD و HH:MM:SS")
                return

            try:
                conn = self._ensure_conn()
                conn.set_time(dt)
                self._finish("تم تغيير وقت وتاريخ جهاز البصمة بنجاح")
            except Exception as e:
                self.conn = None
                self._finish(f"فشل تغيير وقت البصمة: {e}")
        self.status = "جاري تغيير وقت البصمة..."
        self._run_bg(work)

    def sync_now_to_device(self):
        now = datetime.datetime.now()
        self.date_text = now.strftime("%Y-%m-%d")
        self.time_text = now.strftime("%H:%M:%S")
        self.set_device_datetime()

class ZKMobileApp(App):
    def build(self):
        Window.softinput_mode = "below_target"
        Builder.load_string(KV)
        return MainScreen()

if __name__ == "__main__":
    ZKMobileApp().run()
