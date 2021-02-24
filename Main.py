from ChessBot import ChessBot
from tkinter import *
import tkinter.font as font
from functools import partial
import time
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        self.pieces = ['♚','♛','♝','♞', '♜', '     ♟︎', '',
                       '♙', '♖', '♘', '♗', '♕', '♔']

        self.bot = ChessBot()
        self.button = []
        self.button_text = []
        colors = ['white', self._from_rgb((200, 200, 200))]*2
        for i in range(8):
            for j in range(8):
                self.button_text.append(StringVar())
                self.button.append(Button(self, textvariable=self.button_text[-1], 
                                          command=partial(self.clickExitButton, [i,j]),
                                          bg = colors[i%2+j%2],
                                          height = 1, width = 3))
                self.button[-1].grid(row=i,column=j)
                self.button[-1]['font'] = font.Font(size=20)  
                self.button_text[-1].set(self.pieces[-1*self.bot.board[i, j]-7])
                
        self.fromm = ''
        self.to = ''
                
    def _from_rgb(self, rgb):
        """
        translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb
    
    def clickExitButton(self, arg):
        if self.fromm == '':
            self.fromm = self.bot.convert([arg[0], arg[1]])
            print('From ' + self.fromm)
        else:
            self.to = self.bot.convert([arg[0], arg[1]])
            print('to ' + self.to)
            print('')
            self.bot.user_move(self.fromm, self.to, user = 'user', show = False)
            self.set_text()
            time.sleep(0.5)
            self.bot.next_move()
            self.fromm = ''
            self.set_text()
        
    def set_text(self):
        for i in range(8):
            for j in range(8):
                self.button_text[j+8*i].set(self.pieces[-1*self.bot.board[i, j]-7])
                
root = Tk()
app = Window(root)
root.wm_title("Tkinter button")
root.geometry("485x464")
root.mainloop()