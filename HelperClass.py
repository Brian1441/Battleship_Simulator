#Python version 3.6.0
import random as r
from collections import defaultdict
#import numpy as np
#from copy import deepcopy

class HelperFunctions():
    def __init__(self):
        pass

    def kill_ship(self,strike_area):
        self.overall_p_density = self.calculate_strategy()
        while self.open_hits:   #keeps running until all found ships are sunk
            c = self.open_hits[0]
            x , y = c
            x_axis = []
            y_axis= []
            down_list = []
            up_list = []
            r_list = []
            l_list = []

            switch = [1,1,1,1]
            for i in range(1,10): #for the remaining length of the board
                down = (x,c[1]+i)
                up = (x,c[1]-i)
                right = (c[0]+i,y)
                left = (c[0]-i, y)

                #give a contiguous area where ships might be
                #this includes the strike area and self.open_hits
                open_hits_coordinates = list(self.open_hits)
                considered_area = strike_area + open_hits_coordinates
                
                if down in considered_area and switch[0] ==1:
                    down_list.append(down)
                else:
                    switch[0]=0
                if up in considered_area and switch[1] ==1:
                    up_list.append(up)
                else:
                    switch[1]=0
                if right in considered_area and switch[2] ==1:
                    r_list.append(right)
                else:
                    switch[2]=0
                if left in considered_area and switch[3] ==1:
                    l_list.append(left)
                else:
                    switch[3]=0
            #I am only using these memory addresses for identification for my greedy algorithm
            #Python is not meant to manipulate the memory so i am not doing that
            memory_locations = {}
            memory_locations[hex(id(r_list))] =  r_list#(1,0)
            memory_locations[hex(id(l_list))] = l_list#(-1,0)
            memory_locations[hex(id(up_list))] = up_list#(0,-1)
            memory_locations[hex(id(down_list))] = down_list#(0,1)
            
            #obtain the next available square for attack
            #for all directions by removing open hits
            adjustment_set = set() #to keep track of where the open hits are
            exit_condition = 0
            while exit_condition == 0:
                exit_condition = 1
                for i in memory_locations:
                    if len(memory_locations[i]) > 0:
                        if memory_locations[i][0] in self.open_hits:
                            memory_locations[i].pop(0)
                            adjustment_set.add(i)
                            exit_condition = 0
                            
            #find the axes with adjacent open hits
            horizontal_adj = 0
            vertical_adj = 0
            for i in adjustment_set:
                if i in [hex(id(r_list)),hex(id(l_list))]:
                    horizontal_adj = 100
                if i in [hex(id(up_list)),hex(id(down_list))]:
                    vertical_adj = 100

            #obtain the probability densities
            try:
                right_val = self.overall_p_density[r_list[0]]
            except:
                right_val = 0
            try:
                left_val = self.overall_p_density[l_list[0]]
            except:
                left_val=0
            try:
                up_val = self.overall_p_density[up_list[0]]
            except:
                up_val=0
            try:
                down_val = self.overall_p_density[down_list[0]]
            except:
                down_val = 0
                    
            #the preferred axis has adjacent open hits
            if left_val > 0:
                left_val = left_val + horizontal_adj
            if right_val > 0:    
                right_val = right_val + horizontal_adj
            if up_val > 0:
                up_val = up_val + vertical_adj
            if down_val > 0:
                down_val = down_val + vertical_adj
                
            #Select an axis
            if (right_val + left_val) > (up_val + down_val):
                axis=[r_list,l_list]
            elif (right_val + left_val) < (up_val + down_val):
                axis=[up_list,down_list]
            else:
                axis=r.choice([[up_list,down_list],[r_list,l_list]])
            #process the selected axis
            strike_area = self.process_axis(c,axis,strike_area)
        return strike_area        

    def process_axis(self,c,axis, strike_area):
        current_hits=[c]
        visited_directions =set()
        while (len(axis[0]) + len(axis[1])) > 0:
            current_list = self.maxchoice(axis[0],axis[1])   #current_list is a reference to the original list
            if current_list == "skip":
                #probability for both directions is zero
                #return to open hits loop
                break  
            visited_directions.add(hex(id(current_list)))
            attack1 = current_list.pop(0)         
            self.board[attack1[0]][attack1[1]].struck =1
            self.strike_summary.append(attack1)
            strike_area.remove(attack1)
               
            #In the event of a hit
            if self.board[attack1[0]][attack1[1]].occupied ==1:
                current_hits.append(attack1)
                self.open_hits.append(attack1)
                #ship updating
                for i in self.ships:
                    if i.sunk==1:
                        continue
                    new_sunk = i.update(self.board)
                    if new_sunk == 1:
                        self.ships_count = self.ships_count - 1
                        for j in i.location:
                            self.board[j[0]][j[1]].shipsunk = 1
                            try:
                                current_hits.remove((j[0],j[1]))
                            except:
                                pass
                            try:
                                self.open_hits.remove((j[0],j[1]))  
                            except:
                                pass
                        #empty out this direction
                        del current_list[:] #empty out original and reference list
                        #switch to opposite list
                        if hex(id(current_list)) ==hex(id(axis[0])):
                            current_list = axis[1]
                        else:
                            current_list = axis[0]
                        if len(current_hits) <2:  #back to open hits loop if another ship is not suspected
                            del current_list[:]
                        break
             #in the event of a miss    
            else:
                del current_list[:]
            #recalculating strategy after every strike
            self.overall_p_density = self.calculate_strategy()
            #end of axis loop
        return strike_area
          
    def maxchoice(self, list1, list2):
        try:
            a = self.overall_p_density[list1[0]]
        except:
            a = 0
        try:
            b = self.overall_p_density[list2[0]]
        except:
            b=0          
        if a>b:
            return list1
        if a<b:
            return list2
        if b + a == 0:
        #no hit possible so return to the open hits loop
            return "skip"
        if b == a:
            return r.choice([list1,list2])

    def minmax_ships(self):  
        ship_lengths = []
        minimum_ship_length = 0
        maximum_ship_length = 0
        for i in self.ships:
            if i.sunk == 0:
                ship_lengths.append(i.length)
        if ship_lengths:
            minimum_ship_length = min(ship_lengths)
            maximum_ship_length = max(ship_lengths)
        return minimum_ship_length, maximum_ship_length, ship_lengths


    #compute strategy based on the probability density method
    def calculate_strategy(self):
        '''output: probability density'''
        min_ship_length, max_ship_length, available_ships = self.minmax_ships()
        densities = []
        for length in available_ships:
            open_slots,probability_density = self.list_possibilities(length, mode =1)
            densities.append(probability_density)
        overall_p_density = defaultdict(int)
        for i in densities:
            for k in i:
                overall_p_density[k] = overall_p_density[k] + i[k]
        return overall_p_density
