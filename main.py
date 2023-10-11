from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import *
from kivy.animation import Animation
from kivy.uix.image import *
from kivy.lang import Builder
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from datetime import datetime, date


btn_color = (0.48,0.60,0.45,0.9)
class IntrScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        with self.canvas:
            self.rect = Rectangle(source='blurry_river.png', pos=layout.pos, size=self.size) #тут я создаю фон (картинку-прямоугольник)
        self.add_widget(layout)
        instr = Label(text='Вы пребываете в состоянии панической атаки в данный момент?', font_size=21, outline_width=1, outline_color=(0.28,0.40,0.25,1))
        self.btn1=Button(text='Да', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn1.on_press = self.next
        self.btn1.background_color = btn_color
        self.btn2=Button(text='Нет, я хочу просмотреть\nсвои прошлые записи', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn2.on_press = self.records
        self.btn2.background_color = btn_color
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.btn1)
        outer.add_widget(self.btn2)
        self.add_widget(outer)

    def next(self):
        self.manager.current = 'main' #смена экрана

    def records (self):
        self.manager.current='records'

    def resize(self, *_):
        widgets = self.children[:]
        self.canvas.clear()
        self.clear_widgets()
        with self.canvas:
            self.rect = Rectangle(source='blurry_river.png', pos=self.pos, size=self.size) 
        for widget in widgets:
            self.add_widget(widget)
            #почему в киви нет возможности создавать градиенты
    on_size = resize


class MainScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instruction=Label(text="Дышите в такт кругу", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.btn=Button(text='Я чувствую себя лучше', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.background_normal=''
        self.btn.background_color = (0.27,0.38,0.37,1)
        self.btn.on_press = self.next
        img=Image(source='circle.gif', anim_delay=0.10)
        outer = BoxLayout (orientation='vertical', padding=8, spacing=8) 
        outer.add_widget(instruction)
        outer.add_widget(img)  
        outer.add_widget(self.btn)  
        self.add_widget(outer)
        self.cols = 1
        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        with self.canvas.before:
            self.rect = Rectangle(
                source='New Drawing.png',
                size=self.size,
                pos=self.pos
            )
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next(self):
        self.manager.current = 'slider'

class SliderScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lbl1=Label(text="О чем Вы думали во время панической атаки?", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.ti1=TextInput()
        lbl2=Label(text="Что Вы чувствовали во время панической атаки?", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.ti2=TextInput()
        lbl3=Label(text="Как бы Вы оценили дискомфорт причиненный Вам панической атакой?", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.s=Slider(value_track=True, value_track_color=[0.27,0.38,0.37,1], min=0, max=100)
        self.btn1=Button(text='Сохранить', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn1.background_normal=''
        self.btn1.background_color = (0.27,0.38,0.37,1)
        self.btn1.on_press = self.save
        self.btn2=Button(text='На главный экран', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn2.background_normal=''
        self.btn2.background_color = (0.27,0.38,0.37,1)
        self.btn2.on_press = self.next
        outer = BoxLayout (orientation='vertical', padding=8, spacing=8) 
        outer.add_widget(lbl1)
        outer.add_widget(self.ti1)
        outer.add_widget(lbl2)
        outer.add_widget(self.ti2)
        outer.add_widget(lbl3)
        outer.add_widget(self.s)
        outer.add_widget(self.btn1)
        outer.add_widget(self.btn2)
        self.add_widget(outer)
        self.cols = 1
        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        with self.canvas.before:
            self.rect = Rectangle(
                source='New Drawing.png',
                size=self.size,
                pos=self.pos
            )
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next(self):
        self.manager.current = 'intr'
    def save (self):
        dt=datetime.today()
        thoughts=self.ti1.text
        feels=self.ti2.text
        discomfort=self.s.value
        symptoms=str(thoughts)+'+'+str(feels)+'+'+str(discomfort)
        thisstr=str(dt)+'&'+str(symptoms)
        f=open("record.txt", "a+")
        f.write(str(thisstr))
        f.close()
        print (dt)


class RecordsScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lbl1=Label(text="Введите день, запись за который вы хотите получить", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.tirecords=TextInput()
        self.lbl2=Label(text="", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.lbl3=Label(text="", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.lbl4=Label(text="", size_hint_y=0.3, color=[0.27,0.38,0.37,1])
        self.btn1=Button(text='Получить запись', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn1.background_normal=''
        self.btn1.background_color = (0.27,0.38,0.37,1)
        self.btn1.on_press = self.getrecords
        self.btn2=Button(text='На главный экран', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn2.background_normal=''
        self.btn2.background_color = (0.27,0.38,0.37,1)
        self.btn2.on_press = self.next
        outer = BoxLayout (orientation='vertical', padding=8, spacing=8) 
        outer.add_widget(lbl1)
        outer.add_widget(self.tirecords)
        outer.add_widget(self.lbl2)
        outer.add_widget(self.lbl3)
        outer.add_widget(self.lbl4)
        outer.add_widget(self.btn1)
        outer.add_widget(self.btn2)
        self.add_widget(outer)
        self.cols = 1
        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        with self.canvas.before:
            self.rect = Rectangle(
                source='New Drawing.png',
                size=self.size,
                pos=self.pos
            )
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next(self):
        self.manager.current = 'intr'
    def getrecords(self):
        dt=self.tirecords.text
        f=open("record.txt", "r+")
        lines = f.readlines()
        for i in range(len(lines)):
            if str(dt) in lines[i]:
                sole_string=lines[i]
                sole_string=sole_string.split('&')
                print (sole_string)
                symptoms=sole_string[1].split('+')
                print (symptoms)
                self.lbl2.text="В этот день Вы думали о:"+str(symptoms[0])
                self.lbl3.text="В этот день Вы чувствовали:"+str(symptoms[1])
                self.lbl4.text="В этот день Вы оценили свой уровень дискомфорта как:"+str(symptoms[2])

        f.close()
        

class Ptad(App):
    def build(self):
       sm = ScreenManager()
       sm.add_widget(IntrScr(name='intr'))
       sm.add_widget(MainScr(name='main'))
       sm.add_widget(SliderScr(name='slider'))
       sm.add_widget(RecordsScr(name='records'))
       return sm
    

app=Ptad()
app.run()
