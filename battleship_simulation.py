#Python version 3.6.0
import pygame   #PyGame is the SDL GUI
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import random as r
from collections import defaultdict, deque
from HelperClass import HelperFunctions

class Ship():
    '''This is the doc string of the Ship class'''
    def __init__(self,length):
        self.length = length
        self.sunk=0
        self.location=[]
        
    def update(self, game_board):
        #return 1: for sunk
        #return 0: for not sunk
        if self.sunk==1:
            return 0
        hitcount=0
        for i in self.location:
            square0 = game_board[i[0]][i[1]]
            if square0.struck==1:
                hitcount=hitcount+1
        if hitcount == self.length:
            self.sunk=1
            return 1
        return 0
            
class Square():
    def __init__(self):
        self.occupied = 0
        self.struck = 0
        self.shipsunk = 0
        
class Simulator(HelperFunctions):
    def __init__(self):
        self.length = 10
        self.width = 10
        self.board = []
        self.strike_summary = []
        self.open_hits = deque()
        #make the game board
        for i in range(self.length):
            listj = []
            for j in range(self.width):
                temporary = Square()   #the y-axis is upside down
                                          #(0,0) is the upper-left corner
                listj.append(temporary)   
            self.board.append(listj)

    def get_strike_area(self):
        '''returns a list of coordinates'''
        strike_area = []
        for i in range(self.length):
            row = self.board[i]
            for j in range(self.width):
                strikability=0
                strikability = strikability + row[j].struck
                if strikability == 0:
                    strike_area.append((j,i))
        return strike_area

    #this is where the probability distribution is calculated
    def list_possibilities(self,length=1,mode = 0):
        '''   input ship length
              mode 0: for placing ships
              mode 1: for calculating mid-game strategy
        output: possible slots with upper-left square and directions h or z
        output: probability density for each open square   '''
        probability_density = defaultdict(int)
        open_slots = []
        for i in range(self.length):
            for j in range(((self.width)-(length-1))):
                availability=0
                hit_counter = 0 #remove from probability distribution possibilites entirely in open hits
                for k in range(length):
                    a = self.board[j+k][i].occupied
                    b = self.board[j+k][i].struck
                    c = self.board[j+k][i].shipsunk
                    e = (a*b) - c   #this is an open hit if equal to one
                    f = b - e       # this is struck and not in play if equal to one
                    if mode == 0:
                        availability = availability + a
                    if mode == 1:
                        availability = availability + f
                        hit_counter = hit_counter + e
                if availability == 0 and hit_counter < length:
                    open_slots.append((j,i,'horizontal'))
                    for k in range(length):
                        probability_density[((j+k),i)] = probability_density[((j+k),i)] + 1 
        #vertical
        for i in range(((self.length)-(length-1))):
            for j in range(self.width):
                availability=0
                hit_counter = 0
                for k in range(length):
                    a = self.board[j][i + k].occupied
                    b = self.board[j][i + k].struck
                    c = self.board[j][i + k].shipsunk
                    e = (a*b) - c   
                    f = b - e       
                    if mode == 0:
                        availability = availability + a
                    if mode == 1:
                        availability = availability + f
                        hit_counter = hit_counter + e
                if availability == 0 and hit_counter < length:
                    open_slots.append((j,i,'vertical'))
                    for k in range(length):
                        probability_density[(j,(i+k))] = probability_density[(j,(i+k))] + 1
        slot_count = len(open_slots)
        for i in probability_density:
            #this should sum up to the length of the ship
            probability_density[i] = probability_density[i]/slot_count
        return open_slots, probability_density

    def place_ships(self,ships,manual_slots=[]):
        #takes a list of ships
        #assigns the ship location
        #marks the occupied squares on the board
        for j in range(len(ships)):
            open_slots, probability_density = self.list_possibilities(ships[j].length)
            c = r.choice(open_slots)
            if manual_slots:
                c = manual_slots[j] #x,y,horizontal or vertical
            direction = c[2]
            if direction == 'horizontal':
                for i in range(ships[j].length):
                    ships[j].location.append((c[0]+i,c[1]))  #Place ship horizontally
                    self.board[c[0]+i][c[1]].occupied=1
            if direction == 'vertical':
                for i in range(ships[j].length):
                    ships[j].location.append((c[0],c[1]+i))  #Place ship vertically
                    self.board[c[0]][c[1]+i].occupied=1

    def setup(self):
        self.ship1 = Ship(5)
        self.ship2 = Ship(4)
        self.ship3 = Ship(3)
        self.ship4 = Ship(3)
        self.ship5 = Ship(2)
        slots=[]
        c0 = None #first attack specified, default is None
        self.ships = [self.ship1,self.ship2,self.ship3,self.ship4,self.ship5]
        
    def start_simulation(self): #this simulation runs until one strike is made
        ship1 = Ship(5)
        self.ships = [ship1]
        self.ships_count = len(self.ships)
        self.place_ships(self.ships)
        hit = 0
        strike_area = self.get_strike_area()
        while hit ==0:
            c = r.choice(strike_area)           #attack a random open square
            strike_area.remove(c)
            self.board[c[0]][c[1]].struck =1
            self.strike_summary.append(c)
            if self.board[c[0]][c[1]].occupied ==1:
                hit=1

    #This is a full simulation
    def start_simulation2(self,c0=None,slots=[]):
        #self.setup()
        self.ships_count = len(self.ships)
        self.place_ships(self.ships,slots)
        strike_area = self.get_strike_area()
        while self.ships_count > 0:
            c = r.choice(strike_area) #attack a random open square
            if c0:
                c = (c0[0],c0[1])
            strike_area.remove(c)
            self.board[c[0]][c[1]].struck =1
            self.strike_summary.append(c)
            if self.board[c[0]][c[1]].occupied ==1:
                #open hits should always be empty at this stage
                if len(self.open_hits) > 0:
                    print("error:  should not return to main loop while there are open hits")
                self.open_hits.appendleft(c)
                strike_area = self.kill_ship(strike_area=strike_area)
            c0=None

