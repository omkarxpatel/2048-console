# ## todo
# ## left right movement
# ## game end checker
# ## score tracker
# ## moves tracker


# Logic for board movement:
# 1. Get the board into new arrays, based off of direction
# 2. Remove all 0's
# 3. Merge the blocks, based off of direction
# 4. Add 0's again
# 5. Rotate to make board again

# Example (moving to the right):
#     2 0 0 2
#     0 2 2 4
#     2 0 2 4
#     4 2 0 0
    
# Step 1:
#     [2,0,0,2]
#     [0,2,2,4]
#     [2,0,2,4]
#     [4,2,0,0]
    
# Step 2:
#     [2,2]
#     [2,2,4]
#     [2,2,4]
#     [4,2]

# Step 3:
#     [4]
#     [4,4]
#     [4,4]
#     [4,2]

# Step 4:
#     [0,0,0,4]
#     [0,0,4,4]
#     [0,0,4,4]
#     [0,0,4,2]

# Step 5:
#     No rotation needed

import os
import copy
import random
from getkey import getkey, keys
from colorama import Fore, Style

class Game:
    def __init__(self):
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        # self.board = [
        #     [1, 5, 1, 5],
        #     [2, 6, 2, 6],
        #     [3, 7, 3, 7],
        #     [4, 8, 4, 8],
        # ]
        self.points = 0

        self.valid = [2] * 9
        self.valid.append(4) # 90% of a 2 block spawning 10% for a 4 block
        
        # initiation sequence, sets up random squares with starting blocks
        
        values = {}
        while len(values) != 4:
            temp = random.randint(1,16)
            if temp not in values.keys():
                values[temp] = random.choice(self.valid)
        
        values = {1:2, 9:2, 13:4} # debug testing
        # values = {1:2, 5:2, 9:4}
                
        for i in values.keys():
            self.board[(i-1)//4][(i-1)%4] = values[i]
        
    def clear(self):
        os.system('clear')
        
    def getIndices(self, mode): # gets all indices of squares taken by a block
        res = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if mode == 0:
                    if self.board[i][j] == 0:
                        res.append([i, j])
                elif mode == 1:
                    if self.board[i][j] != 0:
                        res.append([i, j])
        return res

    def gameOver(self, valid):
        if len(valid) == 0:
            # exit()
            gameNotOver = False
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    curr = self.board[i][j]
                    indices = []
                    
                    if i > 0:
                        indices.append([i-1,j])
                    if i < 3:
                        indices.append([i+1,j])
                    if j > 0:
                        indices.append([i,j-1])
                    if j < 3:
                        indices.append([i,j+1])
                        
                    for i in range(len(indices)):
                        if self.board[indices[i][0]][indices[i][1]] == curr:
                            gameNotOver = True
                            break
                if gameNotOver == True:
                    break
            if gameNotOver == False:
                self.printBoard(self.board)
                exit()
            # game lost, now do algo to check if fully lost
            
    def placeRandom(self): # places a random block at a random, non-taken square
        valid = self.getIndices(mode=0)
        self.gameOver(valid)
        location = random.choice(valid)
        self.board[location[0]][location[1]] = random.choice(self.valid)

    def removeZeros(self, values):
        temp = []
        for x in values:
            temp.append([i for i in x if i != 0]) # removes 0 in array
        # temp = [[i for i in x if i != 0] for x in values]
        return temp
    
    def moveAll(self, key): # method to move all blocks in a direction pressed by user
        if key in [keys.UP, 'w']:
            print("UP")
            values = [[],[],[],[]]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    values[j].append(self.board[i][j]) # sets up array vertical down

            values = self.removeZeros(values)
            
            for i in range(len(values)): # merges all values
                for j in range(len(values[i])-1):
                    if values[i][j] == values[i][j+1]:
                        values[i][j] *= 2
                        values[i][j+1] = 0
                        
            values = self.removeZeros(values)
            temp = []
            for i in values:
                while len(i) != 4:
                    i.append(0)
                temp.append(i) # makes list back to len 4
            
            res = []
            for i in range(len(temp)): # flips grid over z axis
                t = []
                for j in range(len(temp[i])):
                    t.append(temp[j][i])
                res.append(t)

            self.board = res # sets board to merged board


        elif key in [keys.DOWN, 's']:
            print("DOWN")
            values = [[],[],[],[]]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    values[j].append(self.board[i][j]) # sets up array vertical down

            values = self.removeZeros(values)
            
            for i in range(len(values)): # merges all values
                for j in range(len(values[i])-1, 0, -1):
                    if values[i][j] == values[i][j-1]:
                        values[i][j] *= 2
                        values[i][j-1] = 0
                        
            values = self.removeZeros(values)
            temp = []
            for i in values:
                while len(i) != 4:
                    i.insert(0, 0)
                temp.append(i) # makes list back to len 4
            
            res = []
            for i in range(len(temp)): # flips grid over z axis
                t = []
                for j in range(len(temp[i])):
                    t.append(temp[j][i])
                res.append(t)

            self.board = res # sets board to merged board

                            
        elif key in [keys.RIGHT, 'd']:
            values = self.board

            values = self.removeZeros(values)
            
            for i in range(len(values)): # merges all values
                for j in range(len(values[i])-1):
                    if values[i][j] == values[i][j+1]:
                        values[i][j] *= 2
                        values[i][j+1] = 0
                        
            values = self.removeZeros(values)
            temp = []
            for i in values:
                while len(i) != 4:
                    i.insert(0,0)
                temp.append(i) # makes list back to len 4
            
            self.board = temp # sets board to merged board

        elif key in [keys.LEFT, 'a']:
            print("LEFT")  
            values = self.board

            values = self.removeZeros(values)
            
            for i in range(len(values)): # merges all values
                for j in range(len(values[i])-1, 0, -1):
                    if values[i][j] == values[i][j-1]:
                        values[i][j] *= 2
                        values[i][j-1] = 0
                        
            values = self.removeZeros(values)
            temp = []
            for i in values:
                while len(i) != 4:
                    i.append(0)
                temp.append(i) # makes list back to len 4
            
            self.board = temp # sets board to merged board   

        self.placeRandom()

    def printBoard(self, board): # prints board
        sep = "--------------"
        print(sep)
        count = 0
        for row in board:
            row = [str(i) if i == 0 else f"{Fore.RED}{i}{Style.RESET_ALL}" for i in row]
            print("|", "  ".join(row), "|")

            count += 1
            if count != 4:
                print("|" + " " * (len(sep) - 2) + "|")
        print(sep)
        
        # self.gameOver(self.getIndices(mode=0))


    def main(self): # main loop
        while True:
            self.printBoard(self.board)   
            key = getkey() 
            self.clear()
                
            self.moveAll(key)            
            # self.placeRandom()
            
if __name__ == '__main__':
    Game().main()