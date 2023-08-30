__version__ = "1.0"

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout

from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

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

class CollectablesDrawer(ScrollView):
	pass

class MainWindow(MDFloatLayout):
	
	def __init__(self , **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.card_opener = CardOpener()
	
	


class CollectablesApp(MDApp):
	
	def build(self):
		return Builder.load_file("design.kv")


CollectablesApp().run()

