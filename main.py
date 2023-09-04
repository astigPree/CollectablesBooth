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
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty , NumericProperty , ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as chex

from data_manager import AppManager

COLORS = {
	"SS" : chex("#85200C"),
	"S+" : chex("#85200C"),
	"S" : chex("#85200C"),
	"A+" : chex("#9900FF"),
	"A" : chex("#9900FF"),
	"B+" : chex("#9900FF"),
	"B" : chex("#E69138"),
	"C" : chex("#E69138")
}


class InformationBoard(ModalView):
	user_id : str = StringProperty("627262836")
	cards : int = NumericProperty(0)
	values : int = NumericProperty(0)
	rarity_list : list = ListProperty([0,0,0,0,0,0,0,0])
	
	def on_pre_open(self , *args):
		self.user_id = self.attach_to.app_data.user_info["user_name"]
		self.cards = self.attach_to.app_data.getTotalNumberOfCards()
		self.values = self.attach_to.app_data.getTotalValue()
		for i , value in enumerate(self.attach_to.app_data.getNumberOfRarity()):
			self.rarity_list[i] = value[1]
		
		
class CardOpenerButton(Button):
	command : callable = ObjectProperty()
	
	def on_release(self):
		self.command(self.text)

class CardOpener(ModalView):
	button_list : MDGridLayout = ObjectProperty()
	password : str = StringProperty("")
	warning : str = StringProperty("Number you selected does not exist")
	
	def buttonCommand(self , text):
		if len(self.password) < 10:
			self.password += text
	
	def on_pre_dismiss(self, *args):
		self.password = ""
	
	def on_pre_open(self , *args):
		if not self.button_list.children:
			for num in range(1, 10):
				button = CardOpenerButton()
				button.text = str(num)
				button.command = self.buttonCommand
				self.button_list.add_widget(button)
				

class Card(MDBoxLayout):
	value : str = StringProperty("30")
	quote : str = StringProperty("' mapapatay man kita pira pira, nano kay na haglok ka? '")
	rarity : str = StringProperty("SS")
	card_image : Image = ObjectProperty()
	
	isAnimating : bool = BooleanProperty(False)
	animatingColor = StringProperty("black")
	
	def __init__(self , **kwarhs):
		super(Card, self).__init__(**kwarhs)
	
	def startAnimating(self, *arhs):
		self.isAnimating = True
		self.md_bg_color = self.animatingColor
	
	def stopTheAnimation(self , *arhs):
		self.isAnimating = False
		
		
class CardAnimation(ModalView):
	card : Card = ObjectProperty()
	anim = Animation()
	
	def __init__(self , **kwargs):
		super(CardAnimation, self).__init__(**kwargs)
		self.animate_list = []
		
		duration = 1.5
		transition = "in_bounce"
		expand = True
		for half in range(1 , 21):
			anim = Animation( 
				size = (Window.size[0] * 0.8 , Window.size[1] * 0.8), t=transition , duration = duration / half
				) if expand else Animation( 
				size = (Window.size[0] * 0.2 , Window.size[1] * 0.2) , t=transition , duration = duration / half ) 
			expand = not expand
			self.animate_list.append(anim)
		
		for animate in self.animate_list:
			self.anim += animate
	
	def on_pre_open(self , *args):
		self.card.size = Window.size[0] * 0.2 , Window.size[1] * 0.2
		self.card.startAnimating()
		
		
	def on_open(self , *args):
		self.anim += Animation( md_bg_color = COLORS.get(self.card.rarity) , t="out_quart", size = (Window.size[0] * 0.8 , Window.size[1] * 0.8) , duration = 1 	)
		self.anim.bind(on_complete = self.card.stopTheAnimation )
		self.anim.start(self.card)
	
	
class CollectablesDrawer(ScrollView):
	
	def on_scroll_move(self , *args):
		pass

class MainWindow(MDFloatLayout):
	
	def __init__(self , **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.card_opener = CardOpener()
		self.card_opener.attach_to = self
		self.information_board = InformationBoard()
		self.information_board.attach_to = self
		self.card_anim = CardAnimation()
		self.app_data = AppManager()
	
	#def on_kv_post(self , *arhs):
#		Clock.schedule_once(self.card_anim.open , 1)

class CollectablesApp(MDApp):
	
	def on_start(self):
		self.root.app_data.loadUserInformation()
		self.root.app_data.loadCollections()
	
	def build(self):
		return Builder.load_file("design.kv")



LabelBase.register( name = "poppins_black" ,fn_regular="fonts/Poppins-Black.otf")
LabelBase.register( name = "poppins_bold" ,fn_regular="fonts/Poppins-Bold.otf")
LabelBase.register( name = "poppins_italic" ,fn_regular="fonts/Poppins-Italic.otf")
LabelBase.register( name = "poppins_reg" ,fn_regular="fonts/Poppins-Regular.otf")
CollectablesApp().run()

