from ChessBot import ChessBot
from tkinter import *
import tkinter.font as font
from functools import partial
import time
import numpy as np

class Window(Frame):
    """
    User interface
    
    """
    
    def __init__(self, master=None):
        """
        Initialization
        
        The frame basically exists of 8x8 buttons that change label and color
        
        """
        Frame.__init__(self, master)        
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
        # Pictograms for chess pieces, might not be supported by system
        self.pieces = ['♚','♛','♝','♞', '♜', '     ♟︎', '',
                       '♙', '♖', '♘', '♗', '♕', '♔']
        
        # Setup the chessbot
        self.bot = ChessBot()
        
        # Setup the buttons
        self.button = []
        self.button_text = []
        self.colors = ['white', self._from_rgb((200, 200, 200))]*2
        for i in range(8):
            for j in range(8):
                self.button_text.append(StringVar())
                self.button.append(Button(self, 
                                          textvariable=self.button_text[-1], 
                                          command=partial(self.clickExitButton, 
                                                          [i,j]),
                                          bg = self.colors[i%2+j%2],
                                          height = 1, width = 3))
                self.button[-1].grid(row=i,column=j)
                self.button[-1]['font'] = font.Font(size=20)  
                self.button_text[-1].set(self.pieces[-1*self.bot.board[i, j]-7])
           
        # fromm and to track where the last move of the user
        self.fromm = ''
        self.to = ''
                
    def _from_rgb(self, rgb):
        """
        translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb
    
    def clickExitButton(self, arg):
        """
        Action to perform on button click. 
        
        Inputs:
            arg: the location of the button that is clicked.

        """
        
        # If fromm is empty, the piece is selected. If froom is not empty,
        # the user is selecting the place to go
        if self.fromm == '':
            self.fromm = self.bot.convert([arg[0], arg[1]])
            self.fromm_loc = arg[0]*8+arg[1]
            
            # Highlight the button
            self.button[self.fromm_loc].configure(bg="yellow") 
            print('From ' + self.fromm)
        else:
            self.to = self.bot.convert([arg[0], arg[1]])
            self.to_loc = arg[0]*8+arg[1]
            print('to ' + self.to)
            print('')
            
            # Request the move in the bot
            status = self.bot.user_move(self.fromm, 
                                        self.to, user = 'user', show = False)
            
            # If approved, move the bot, if not, color it red
            if status:
                self.button[self.fromm_loc].configure(bg="green") 
                self.button[self.to_loc].configure(bg="yellow") 
                self.set_text()
                self.update()
                self.check_check()
                start, self.end = self.bot.next_move()
                self.reset_background()
                self.button[start[0]*8+start[1]].configure(bg="green") 
                self.button[self.end[0]*8+self.end[1]].configure(bg="yellow")
                self.check_check()
            else:
                self.button[self.fromm_loc].configure(bg="red") 
            
            # Wait a bit and reset the background colors
            self.update()
            time.sleep(0.5)
            self.reset_background()
            self.fromm = ''
            self.set_text()
            

    def check_check(self):
        if not np.any(self.bot.board == 6) or not np.any(self.bot.board == -6):
            self.button[self.to_loc].configure(bg="red")
            self.update()
            time.sleep(5)
            self.destroy()
            
    def set_text(self):
        """
        Updates the labels of all the buttons based on bot.board

        """
        for i in range(8):
            for j in range(8):
                self.button_text[j+8*i].set(self.pieces[-1*self.bot.board[i, 
                                                                          j]-7])
                
    def reset_background(self):
        """
        Reset the pattern of the board

        """
        for i in range(8):
            for j in range(8):
                self.button[j*8+i].configure(bg=self.colors[i%2+j%2]) 
                
root = Tk()
app = Window(root)
root.wm_title("Chess bot")
root.geometry("485x464")
root.mainloop()
