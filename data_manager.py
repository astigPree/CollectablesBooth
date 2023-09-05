import json
import typing as tp
import os
from uuid import uuid4
import random

"""
    Card Information:
        - rarity ; ( SS, S+, S , A+ , A , B+ , B , C )
        - picture ; file location
        - quote ; 
        - value ; card number value
    
    Collectables Data Structure:
        HIGH : SS, S+, S
        MID : A+ , A , B+
        LOW : B , C
        
        { 
            'high' : [ ( rarity, picture, quote, value ), .. ],
            'mid' : [ ( rarity, picture, quote, value ), .. ],
            'low' : [ ( rarity, picture, quote, value ), .. ]
        }
    
    Collections Data Structure:
        {
            'SS' : [ ( rarity, picture, quote, value ), ... ],
            'S+' : [ ( rarity, picture, quote, value ), ... ],
            'S' : [ ( rarity, picture, quote, value ), ... ],
            'A+' : [ ( rarity, picture, quote, value ), ... ],
            'A' : [ ( rarity, picture, quote, value ), ... ],
            'B+' : [ ( rarity, picture, quote, value ), ... ],
            'B' : [ ( rarity, picture, quote, value ), ... ],
            'C' : [ ( rarity, picture, quote, value ), ... ],
        }
    
    User Information Data Structure:
        {
            username : str,
        }
    
"""
COLLECTION_FILE = "collection.json"
COLLECTABLES_FILE = "collectables.json"
USER_FILE = "user_information.json"
PICTURE_FOLDER = "pictures"

LIST_OF_RARITY = ("SS" , "S+" , "S" , "A+" , "A" , "B+" , "B" , "C") # Highest to Lowest


class AppManager :
    collectables: tp.Dict = None
    collections: tp.Dict = None
    user_info : tp.Dict = None

    high_password = "45678"
    mid_password = "6789"
    low_password = "12345"

    def loadUserInformation(self):
        if not os.path.exists(USER_FILE):
            user_info = { "user_name" : str(uuid4())[:10] }
            with open(USER_FILE , 'w') as jf:
                json.dump(user_info , jf)

        with open(USER_FILE , 'r') as jf:
            self.user_info = json.load(jf)

    def saveUserInformation(self):
        with open(USER_FILE , "w") as jf:
            json.dump(self.user_info , jf)

    def loadCollections(self) :
        with open(COLLECTION_FILE, 'r') as jf :
            self.collections = json.load(jf)

    def saveCollections(self):
        with open(COLLECTION_FILE , 'w') as jf:
            json.dump(self.collections , jf)

    def loadCollectables(self) :
        if self.collectables is not None: return

        with open(COLLECTABLES_FILE, 'r') as jf :
            self.collectables = json.load(jf)

    def getTotalNumberOfCards(self) -> int :
        total = 0
        for key in self.collections :
            total += len(self.collections[key])
        return total

    def getNumberOfRarity(self) -> list[tuple[str, int], ...] :
        return [(rarity, len(self.collections[rarity])) for rarity in self.collections]

    def getTotalValue(self) -> int:
        total = 0
        for rarity in self.collections:
            for card in self.collections[rarity]:
                total += int(card[3])
        return total

    def getHighCard(self , password : str) -> tp.Union[None , tuple , bool]:
        if password != self.high_password:
            return None # its mean incorrect password

        cards = [ card for card in self.collectables['high'] if card not in self.collections['SS'] and card not in self.collections['S+'] and card not in self.collections['S'] ]
        if not cards:
            return True # its mean you already get all the card in this tier

        new_card = random.choice(cards)
        self.collections[new_card[0]].append(new_card)
        return new_card # its mean you get a new card

    def getMidCard(self, password : str ):
        if password != self.mid_password:
            return None # its mean incorrect password

        cards = [ card for card in self.collectables['mid'] if card not in self.collections['A'] and card not in self.collections['A+'] and card not in self.collections['B+'] ]
        if not cards:
            return True # its mean you already get all the card in this tier

        new_card = random.choice(cards)
        self.collections[new_card[0]].append(new_card)
        return new_card # its mean you get a new card

    def getLowCard(self , password : str):
        if password != self.low_password:
            return None # its mean incorrect password

        cards = [ card for card in self.collectables['low'] if card not in self.collections['B'] and card not in self.collections['C']]
        if not cards:
            return True # its mean you already get all the card in this tier

        new_card = random.choice(cards)
        self.collections[new_card[0]].append(new_card)
        return new_card # its mean you get a new card
     
    def addCardToCollections(self , rarity : str , card : tuple):
    	self.collections[rarity].append(card)
	
	
test = AppManager()
test.loadCollectables()
test.loadCollections()
test.loadUserInformation()
print(test.getLowCard("12345"))
