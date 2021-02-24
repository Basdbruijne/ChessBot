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
        self.colors = ['white', self._from_rgb((200, 200, 200))]*2
        for i in range(8):
            for j in range(8):
                self.button_text.append(StringVar())
                self.button.append(Button(self, textvariable=self.button_text[-1], 
                                          command=partial(self.clickExitButton, [i,j]),
                                          bg = self.colors[i%2+j%2],
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
            self.fromm_loc = arg[0]*8+arg[1]
            self.button[self.fromm_loc].configure(bg="yellow") 
            print('From ' + self.fromm)
        else:
            self.to = self.bot.convert([arg[0], arg[1]])
            self.to_loc = arg[0]*8+arg[1]
            print('to ' + self.to)
            print('')
            status = self.bot.user_move(self.fromm, self.to, user = 'user', show = False)
            if status:
                self.button[self.fromm_loc].configure(bg="green") 
                self.button[self.to_loc].configure(bg="yellow") 
                self.set_text()
                self.update()
                start, end = self.bot.next_move()
                self.reset_background()
                self.button[start[0]*8+start[1]].configure(bg="green") 
                self.button[end[0]*8+end[1]].configure(bg="yellow") 
            else:
                self.button[self.fromm_loc].configure(bg="red") 
            
            self.update()
            time.sleep(0.5)
            self.reset_background()
            self.fromm = ''
            self.set_text()
        
    def set_text(self):
        for i in range(8):
            for j in range(8):
                self.button_text[j+8*i].set(self.pieces[-1*self.bot.board[i, j]-7])
                
    def reset_background(self):
        for i in range(8):
            for j in range(8):
                self.button[j*8+i].configure(bg=self.colors[i%2+j%2]) 
                
root = Tk()
app = Window(root)
root.wm_title("Chess bot")
root.geometry("485x464")
root.mainloop()
