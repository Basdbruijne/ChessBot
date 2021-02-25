
import numpy as np
from termcolor import colored
import random
from copy import deepcopy as copy
import concurrent.futures

class ChessBot():
    """
    Class Chatbot contains 2 key functions:
        bot = ChessBot()
        
        bot.user_move('A2', 'A2') # <- make your move
        bot.next_move() # <- bot makes the move
                
    """
    def __init__(self, depth = 0):
        """
        Initialize code:
            
        inputs: 
            depth: Only used for predictions, not to be specified by user 

        """
        
        self.depth = depth
        self.color = 'white' # color that the user plays with, will be 
                             # changable in future versions
        self.color_user = None
        
        # the board is an array with numbers that corresponds to the piece 
        # thats on it. Positive number is bot, negative is user
        self.board = np.array([[2, 3, 4, 5, 6, 4, 3, 2],                 
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        
        self.board -= self.board[::-1]
        
        # convert_dict is used for the conversion of e.g. 'A1' to location on 
        # the matrix in self.board
        self.convert_dict = {}
        for i in range(0, 8):
            self.convert_dict[chr(65+i)] = i
            self.convert_dict[i] = chr(65+i)
        
    def show_board(self):
        """
        Prints the board in a way that is more-or-less understandable to humans
                            
        """
        
        print(colored('   A B C D E F G H'))
        print(colored('   ---------------'))
        
        pieces = ['', 'P', 'R', 'N', 'B', 'Q', 'K']
        for i in range(8):
            row = colored(str(8-i) + '| ')
            for j in range(8):
                if not pieces[abs(self.board[i, j])] == '':
                    if self.board[i, j] < 0:
                        color = self.color
                    else:
                        color = self.color_user 
                    row += colored(str(pieces[abs(self.board[i, j])])+' ', 
                                   color)
                else:
                    row += colored(pieces[0]+'  ', self.color)
            print(row)
        
    def convert(self, x, user = 'self'):
        """
        Converts board location (e.g. 'A1') to matrix index (e.g. [0,0])
        inputs:
            x:  either string (e.g. 'A1' or array (e.g. [0,0])
            user: either 'self' being bot, or 'user'
            
        outputs:
            y: either string (e.g. 'A1' or array (e.g. [0,0]), the other one 
               than the input
                            
        """
        
        if type(x) == str:
            if user == 'self':
                return [8-int(x[1]), self.convert_dict[x[0]]]
            elif user == 'user':
                return [1+int(x[1]), self.convert_dict[x[0]]]
        elif type(x) == list and [8, 8] > x >= [0, 0]:
            if user == 'self':
                return self.convert_dict[x[1]] + str(8-x[0])
            elif user == 'user':
                return self.convert_dict[x[1]] + str(1+x[0])
        else:
            raise TypeError('Invalid type')
                        
    def get_available_moves(self, user):
        """
        Show available moves
        inputs:
            user: either 'self' being bot, or 'user'
            
        outputs:
            moves [dict]: keys are the current locations that can be moved,
                          values are the locations that that key can move to.
                          
        TODO: 
            add casting
                            
        """
        moves = {}
        if user == 'user':
            board = -self.board[::-1]
        elif user == 'self':
            board = self.board
        else:
            raise TypeError('User not recognized, specify "user" or "self"')
        for i in range(8):
            for j in range(8):
                move_curr = []
                """ Pawn """
                if board[i, j] == 1:
                    if i == 7:
                        continue
                    if board[i+1, j] == 0:
                        move_curr.append(self.convert([i+1, j], user))
                    if i == 1 and board[i+1, j] == 0 and board[i+2, j] == 0:
                        move_curr.append(self.convert([i+2, j], user))
                    if j > 0 and board[i+1, j-1] < 0:
                        move_curr.append(self.convert([i+1, j-1], user))
                    if j < 7 and board[i+1, j+1] < 0:
                        move_curr.append(self.convert([i+1, j+1], user))
                        
                """ Rook, Queen and King """
                if board[i, j] in [2, 5, 6]:
                    ranges = [range(i+1, 8), range(i-1, -1, -1)]
                    for ran in ranges:
                        for ii in ran: 
                            if board[ii, j] == 0:
                                move_curr.append(self.convert([ii, j], user))
                                if board[i, j] == 6:
                                    break
                            elif board[ii, j] < 0:
                                move_curr.append(self.convert([ii, j], user))
                                break
                            else:
                                break
                            
                    ranges = [range(j+1, 8), range(j-1, -1, -1)]
                    for ran in ranges:
                        for jj in ran: 
                            if board[i, jj] == 0:
                                move_curr.append(self.convert([i, jj], user))
                                if board[i, j] == 6:
                                    break
                            elif board[i, jj] < 0:
                                move_curr.append(self.convert([i, jj], user))
                                break
                            else:
                                break
                
                """ Knight """
                if board[i, j] == 3:
                    signs = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
                    movess = [[2, 1], [1, 2]]
                    for move_i, move_j in movess:
                        for sign_i, sign_j in signs:
                            try:
                                if board[i+move_i*sign_i, j+move_j*sign_j] <= 0:
                                    move_curr.append(self.convert([i+move_i*sign_i, 
                                                  j+move_j*sign_j], user))
                            except:
                                continue
                
                """ Bisshop, Queen and King """
                if board[i, j] in [4, 5, 6]:
                    signs = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
                    for sign_i, sign_j in signs:
                        for n in range(1, 8):
                            try:
                                if board[i+sign_i*n, j+sign_j*n] == 0:
                                    move_curr.append(self.convert([i+sign_i*n, 
                                                                   j+sign_j*n], 
                                                                  user))
                                    if board[i, j] == 6:
                                        break
                                elif board[i+sign_i*n, j+sign_j*n] < 0:
                                    move_curr.append(self.convert([i+sign_i*n, 
                                                                   j+sign_j*n], 
                                                                  user))
                                    break
                                else:
                                    break
                            except:
                                break
                
                if move_curr:
                    moves[self.convert([i, j], user)] = move_curr
                
        return moves
    
    def user_move(self, start, end, user = 'user', show = True):
        """
        Request move
        inputs:
            start: piece to move (e.g. 'A2')
            end: location to move to (e.g. 'A4')
            user: either 'self' being bot, or 'user'
            show [bool]: wether or not to show to board
            
        outputs:
            status: 0 - Move not possible
                    1 - Succes
                            
        """
        start = start.upper()
        end = end.upper()
        moves = self.get_available_moves(user = user)
        try:
            moves[start]
        except KeyError:
            start_c = self.convert(start)
            if self.board[start_c[0], start_c[1]] < 0:
                print(start + ' cannot move at this point')
            else:
                print('No piece is found on the selected position')
            return 0
        except:
            raise
            
        if end in moves[start]:
            end_c = self.convert(end)
            start_c = self.convert(start)
            self.board[end_c[0], end_c[1]] = self.board[start_c[0], start_c[1]]
            self.board[start_c[0], start_c[1]] = 0
        else:
            print("This piece can't be moved there, available moves from " + 
                  start + " are " + str(moves[start]))
            return 0
            
        if np.any(self.board[0, :] == -1):
            self.board[0, self.board[0,:] == -1] = -5
            
        if np.any(self.board[-1, :] == 1):
            self.board[-1, self.board[-1,:] == 1] = 5
        
        if show:
            self.show_board()
            
        return 1
        
    def random_move(self):
        """
        Make the bot do a random move
        """
        moves = self.get_available_moves(user = 'self')
        start, ends = random.choice(list(moves.items()))
        end = random.choice(ends)
        self.user_move(start, end, user='self')
        
    def board_score(self, depth):
        """
        Score the board for the bot to evaluate how its doing.
        Inputs:
            None
            
        Output:
            Score: Higher is better for bot
            
        TODO:
            Tweak score to improve the bot
        """
        board = copy(self.board)
        advantage = 5
        board[board == 2] = 4*advantage
        board[board == 3] = 4*advantage
        board[board == 4] = 4*advantage
        board[board == 5] = 8*advantage
        board[board == 6] = 1000*advantage
        board[board == -2] = -4
        board[board == -3] = -4
        board[board == -4] = -4
        board[board == -5] = -8
        board[board == -6] = -1000
        
        score = np.sum(board)
        
        if depth % 1:
            moves = self.get_available_moves('user')
        else:
            moves = self.get_available_moves('user')
            
            for move in moves:
                for new_move in moves[move]:
                    location = self.convert(new_move)
                    score -= board[location[0], location[1]]
            
        return score
        
    def walk_board(self, depth = 0, board = None, s = '', user = 'self', score = 0):
        """
        'Walk' the board. I.e. evaluate all possible moves upto a certain depth
        Inputs:
            DO NOT PASS ANY VARIABLE IN THIS FUNCTION
            all parameters are used for backtracking
            
            depth: used by bot to track how many
                   move deep it is evaluating
            board: Provide board
            s: list of moves
            user: 'self' or 'user', used for alternating
            score: score of the list of moves
        Output:
            s: list of possible moves with score attatched
        """
        global _score
        subbot = ChessBot(depth = self.depth+1)
        if board is None:
            subbot.board = copy(self.board)
        else:
            subbot.board = board
            
        board_original = copy(subbot.board)
        if user == 'self':
            user_next = 'user'
        else:
            user_next = 'self'
        
        if depth == 2:
            return [score, s]
        
        _score = max(_score, score)
        
        # if score > 100 and depth > 0:
        #     return [-100, ""]
        
        new_s = []
        moves = subbot.get_available_moves(user)
        
        for move in moves:
            for next_move in moves[move]:
                subbot.board = copy(board_original)
                subbot.user_move(move, next_move, user=user, show=False)
                if depth == 0:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(subbot.walk_board, 
                                                 depth = depth+1, 
                                              board = subbot.board, 
                                              s = s + move + next_move, 
                                              user = user_next,
                                              score = score 
                                              + subbot.board_score(depth))
                        new_s += future.result()
                else:
                    new_s += subbot.walk_board(depth = depth+1, 
                                                  board = subbot.board, 
                                                  s = s + move + next_move, 
                                                  user = user_next,
                                                  score = score 
                                                  + subbot.board_score(depth))
        return new_s
    
    def next_move(self):
        """
        Make the bot do its next move

        """
        global _score
        s = self.walk_board()
        _score = 0
        move = s[s.index(max(s[::2]))+1]

        while np.random.rand()>.5:
            try:
                del s[s.index(max(s[::2])):s.index(max(s[::2]))+2]
                move = s[s.index(max(s[::2]))+1]
                move = s[s.index(0)+1]
            except:
                break
        self.user_move(move[0:2], move[2:4], user = 'self', show=False)
        
        return self.convert(move[0:2]), self.convert(move[2:4])
                
_score = 0
