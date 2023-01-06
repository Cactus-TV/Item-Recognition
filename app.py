from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import cv2
from ner import neyro
from kivy.uix.camera import Camera 
from kivy.uix.widget import Widget   
from kivy.config import Config
import os
import numpy as np
from PIL import Image as Image1
        
class KivyCamera(Image):
    def __init__(self, capture, fps, resolution, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class CamApp(BoxLayout):
    def __init__(self,  ** kwargs): 
        super(CamApp,  self).__init__(**kwargs) 
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30, resolution = (1920,1080), pos_hint= {'center_x': .5, 'center_y': 1})
        self.add_widget(self.my_camera)
        btn1 = Button(text ='TAKE A PHOTO', size_hint=(1,.1),
                   background_color =(1, 1, 1, 1), 
                   color =(1, 1, 1, 1)) 
        btn1.bind(on_press = self.callback)
        self.add_widget(btn1)
    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
    def callback(self, instance):
        ret, frame = self.capture.read()
        # frame1 = np.asarray(frame)
        # destRGB = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        # img2 = Image1.fromarray(destRGB)
        # img2.transpose(Image1.FLIP_TOP_BOTTOM)
        # img2.show()
        cv2.imwrite(os.path.dirname(__file__)+"\\img.png", frame)
        neyro()
                        
class App(App):
    def build(self):
        Config.set('graphics', 'resizable', '0')
        Config.set('graphics', 'width', '640')
        Config.set('graphics', 'height', '640')
        bx = CamApp()
        bx.orientation='vertical'
        bx.padding = 0
        return bx

App().run()
