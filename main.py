from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty

class Home(Factory.BoxLayout):
    evt = None
    status = StringProperty("Iniciar")
    speed = NumericProperty(.0004)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        start = lambda evt: self.open_text()
        Clock.schedule_once(start)

    def open_text(self):
        with open('roteiro.txt', 'r', encoding="utf-8") as texto:
            self.ids.texto.text = texto.read()

    def start_slide_screen(self):
        def scroll(evt):
            if self.ids.scrollview.scroll_y <= 0:
                self.stop_slide_screen()
                return
            self.ids.scrollview.scroll_y -= self.speed
        self.evt = Clock.schedule_interval(scroll, .1)
        self.status = "Parar"

    def stop_slide_screen(self):
        Clock.unschedule(self.evt)
        self.status = "Iniciar"

class TeleApp(App):
    def build(self):
        return Builder.load_string("""
Home:
    orientation: "vertical"
    padding: dp(10)
    ScrollView:
        id: scrollview
        size_hint: [1,.9]
        BoxLayout:
            orientation: "vertical"
            size_hint: [1, None]
            height: self.minimum_height
            canvas.before:
                Color:
                    rgba: [0,0,0,1]
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: texto
                color: [1,1,1,1]
                font_size: sp(30)
                bold: True
                text: ' gdfg'
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
    BoxLayout:
        size_hint: [1,.1]
        BoxLayout:
            Button:
                text: "-"
                on_release:
                    root.speed -= .0001
            Label:
                text: "%f" % root.speed
            Button:
                text: "+"
                on_release:
                    root.speed += .0001
        Button:
            text: "Carregar"
            on_release:
                root.open_text() 
        Button:
            text: root.status
            on_release:
                root.start_slide_screen() \
                    if root.status == "Iniciar" \
                    else root.stop_slide_screen()
""")

TeleApp().run()