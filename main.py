__version__ = "1.0"

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.animation import Animation

class InformationBoard(ModalView):
	pass

class CardOpenerButton(Button):
	pass

class CardOpener(ModalView):
	button_list : MDGridLayout = ObjectProperty()
	
	def on_pre_open(self , *args):
		if not self.button_list.children:
			for num in range(9):
				button = CardOpenerButton()
				button.text = str(num)
				self.button_list.add_widget(button)
				

class Card(MDBoxLayout):
	value : str = StringProperty("30")
	quote : str = StringProperty("' mapapatay man kita pira pira, nano kay na haglok ka? '")
	rarity : str = StringProperty("B+")
	card_image : Image = ObjectProperty()

class CardAnimation(ModalView):
	card : Card = ObjectProperty()
	
	def on_pre_open(self , *args):
		pass
	
	
class CollectablesDrawer(ScrollView):
	
	def on_scroll_move(self , *args):
		pass

class MainWindow(MDFloatLayout):
	
	def __init__(self , **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.card_opener = CardOpener()
		self.card_opener.attach_to = self
		self.information_board = InformationBoard()
		self.card_anim = CardAnimation()
	
	def on_kv_post(self , *arhs):
		Clock.schedule_once(self.card_anim.open , 1)

class CollectablesApp(MDApp):
	
	def build(self):
		return Builder.load_file("design.kv")



LabelBase.register( name = "poppins_black" ,fn_regular="fonts/Poppins-Black.otf")
LabelBase.register( name = "poppins_bold" ,fn_regular="fonts/Poppins-Bold.otf")
LabelBase.register( name = "poppins_italic" ,fn_regular="fonts/Poppins-Italic.otf")
CollectablesApp().run()

