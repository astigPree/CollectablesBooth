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

from data_manager import AppManager , LIST_OF_RARITY

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
	
	holder : object = ObjectProperty(None)
	
	def on_pre_open(self , *args):
		self.user_id = self.holder.app_data.user_info["user_name"]
		self.cards = self.holder.app_data.getTotalNumberOfCards()
		self.values = self.holder.app_data.getTotalValue()
		for i , value in enumerate(self.holder.app_data.getNumberOfRarity()):
			self.rarity_list[i] = value[1]
		
		
class CardOpenerButton(Button):
	command : callable = ObjectProperty()
	
	def on_release(self):
		self.command(self.text)

class CardOpener(ModalView):
	button_list : MDGridLayout = ObjectProperty()
	password : str = StringProperty("")
	warning : str = StringProperty("")
	
	holder : object = ObjectProperty(None)
	
	def checkNewCard(self , card : object , tier : str):
		if isinstance(card , bool):
			if tier == "low":
				self.warning = "You already get all card in LOW TIER!"
			elif tier == "mid" :
				self.warning = "You already get all card in MIDDLE TIER!"
			else:
				self.warning = "You already get all card in HIGH TIER!"
		else:
			self.holder.saveCardTransaction(card)
			self.holder.card_anim.setValueOfCard(card)
			self.dismiss()
			self.holder.card_anim.open()
	
	def getNewCard(self ):
		# Get a card for low tier
		card = self.holder.app_data.getLowCard(self.password)
		if card:
			self.checkNewCard(card , "low")
			return
		
		# Get a card for mid tier
		card = self.holder.app_data.getMidCard(self.password)
		if card:
			self.checkNewCard(card , "mid")
			return
		
		# Get a card for high tier
		card = self.holder.app_data.getHighCard(self.password)
		if card:
			self.checkNewCard(card , "high")
			return
			
		self.warning = "You Input A Wrong Password!"
		
	
	def buttonCommand(self , text):
		if len(self.password) < 10:
			self.password += text
	
	def on_pre_dismiss(self, *args):
		self.password = ""
		self.warning = ""
	
	def on_pre_open(self , *args):
		if not self.holder.app_data.collectables:
			self.holder.app_data.loadCollectables()
			
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
		
	def setValueOfCard(self , card : tuple):
		self.card.rarity = card[0]
		self.card.card_image.source = card[1]
		self.card.quote = card[2]
		self.card.value = card[3]
	
	def on_pre_open(self , *args):
		if not self.self.card.opacity:
			self.card.opacity = 1
		self.card.size = Window.size[0] * 0.2 , Window.size[1] * 0.2
		self.card.startAnimating()
		
		
	def on_open(self , *args):
		self.anim += Animation( md_bg_color = COLORS.get(self.card.rarity) , t="out_quart", size = (Window.size[0] * 0.8 , Window.size[1] * 0.8) , duration = 1 	)
		self.anim.bind(on_complete = self.card.stopTheAnimation )
		self.anim.start(self.card)
	


class MainWindow(MDFloatLayout):
	
	drawer : MDGridLayout = ObjectProperty()
	
	def __init__(self , **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.card_opener = CardOpener()
		self.card_opener.holder = self
		self.information_board = InformationBoard()
		self.information_board.holder = self
		self.card_anim = CardAnimation()
		self.app_data = AppManager()
	
	def saveCardTransaction(self ,  card : tuple):
		self.app_data.addCardToCollections(rarity=card[0] , card=card)
		self.app_data.saveCollections()
	
	def addDisplayNewCard(self , card : tuple):
		widget = Card()
		widget.rarity , widget.card_image.source, widget.quote , widget.value = card
		
		# if the drawer empty
		if not self.drawer.children:
			self.drawer.add_widget(widget)
		
		collections = self.app_data.getNumberOfRarity()
		pos = 0
		for card in collections:
			
		
		
	def displayAllCollections(self , *args):
		animate = Animation(opacity = 1 , duration = 0.3)
		for rarity in LIST_OF_RARITY:
			for card in self.app_data.collections[rarity]:
				widget = Card()
				widget.md_bg_color = COLORS[rarity]
				widget.rarity , widget.card_image.source, widget.quote , widget.value = card
				self.drawer.add_widget(widget)
				animate.start(widget)
		
	
class CollectablesApp(MDApp):
	
	def on_start(self):
		self.root.app_data.loadUserInformation()
		self.root.app_data.loadCollections()
		Clock.schedule_once(self.root.displayAllCollections , 1)
		
	def build(self):
		return Builder.load_file("design.kv")



LabelBase.register( name = "poppins_black" ,fn_regular="fonts/Poppins-Black.otf")
LabelBase.register( name = "poppins_bold" ,fn_regular="fonts/Poppins-Bold.otf")
LabelBase.register( name = "poppins_italic" ,fn_regular="fonts/Poppins-Italic.otf")
LabelBase.register( name = "poppins_reg" ,fn_regular="fonts/Poppins-Regular.otf")
CollectablesApp().run()

