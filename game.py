import random
import numpy as np
import copy
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']


    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1] #AI

    def succ(self,state): ## only generate for the max player
        """ Takes in board, returns all the legal subsequent successors -> of list type 
        if dropphase true: just all the possible adjacent states
        else: all the possible movements of the all the current states
        """
        ## use the self.opp
        ## on drophase
        lst = []
        if (self.drop_phase):
            # check each cell where can AI put a new successor
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if (state[i][j] ==' '):
                        lst.append([i,j])
        else:
            dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1)] ## all the directions that AI can move
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if (state[i][j] == self.my_piece): ## if it's AI piece
                        # consider all the direction
                        for dir in dirs:
                            # if the state + direction is blank and not out of range
                            if 0 <= i + dir[0] <= 4 and 0 <= j + dir[1] <= 4 and state[i + dir[0]][j + dir[1]] == " ":
                                lst.append([i, j])

        
        return lst
    

                                

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        self.drop_phase = True  # TODO: detect drop phase
        cnt = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] !=" ":
                    cnt +=1
        if (cnt >= 8):
            self.drop_phase = False

        if self.drop_phase:
            # Drop phase: Place a new piece on the board
            best_move = None
            best_score = float("-inf")
            for move in self.succ(state):
                # Deep copy of the state
                temp_state = copy.deepcopy(state)
                temp_state[move[0]][move[1]] = self.my_piece
                score = self.Min_Value(temp_state, 1)
                if score > best_score:
                    best_score = score
                    best_move = move
            # Return move with placeholder for source position
            return [(best_move[0], best_move[1])]
    
        else:
            # Move phase: Move an existing piece
            best_move = None
            best_score = float("-inf")
            for src_row in range(5):
                for src_col in range(5):
                    if state[src_row][src_col] == self.my_piece:
                        # Check all possible moves from the current piece
                        for move in self.succ(state):
                            # Deep copy of the state
                            temp_state = copy.deepcopy(state)
                            # Remove the piece from the source
                            temp_state[src_row][src_col] = ' '
                            # Place the piece at the destination
                            temp_state[move[0]][move[1]] = self.my_piece
                            score = self.Min_Value(temp_state, 1)
                            if score > best_score:
                                best_score = score
                                best_move = (move[0], move[1], src_row, src_col)
            # Return move with source and destination positions
            return [(best_move[0], best_move[1]), (best_move[2], best_move[3])]

        
        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1: #move phase
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
    
    def heuristic_game_value(self, state):
        mymax, oppmax = 0, 0
        mine, oppo = ('b', 'r') if self.my_piece == 'b' else ('r', 'b')
        # Check for horizontal, vertical, and both diagonals
        for i in range(5):
            mycnt_h, oppcnt_h = 0, 0  
            mycnt_v, oppcnt_v = 0, 0

            for j in range(5):
                # Horizontal
                if state[i][j] == mine:
                    mycnt_h += 1
                if state[i][j] == oppo:
                    oppcnt_h += 1

                # Vertical
                if state[j][i] == mine:
                    mycnt_v += 1
                if state[j][i] == oppo:
                    oppcnt_v += 1
            # Update max counters after each row and column
            mymax = max(mymax, mycnt_h, mycnt_v)
            oppmax = max(oppmax, oppcnt_h, oppcnt_v)
        # Check for diagonals and 2x2 squares
        for row in range(5):
            for col in range(5):
                # Diagonals and 2x2 squares
                mycnt_d1, oppcnt_d1 = 0, 0  # Diagonal /
                mycnt_d2, oppcnt_d2 = 0, 0  # Diagonal \
                mycnt_sq, oppcnt_sq = 0, 0  # 2x2 square

                for d in range(4):  # Diagonal and square check within bounds
                    if row + d < 5 and col + d < 5:
                        if state[row + d][col + d] == mine:
                            mycnt_d2 += 1
                        if state[row + d][col + d] == oppo:
                            oppcnt_d2 += 1

                    if row + d < 5 and col - d >= 0:
                        if state[row + d][col - d] == mine:
                            mycnt_d1 += 1
                        if state[row + d][col - d] == oppo:
                            oppcnt_d1 += 1

                    if row + 1 < 5 and col + 1 < 5:
                        if state[row][col] == mine and state[row + 1][col] == mine and \
                        state[row][col + 1] == mine and state[row + 1][col + 1] == mine:
                            mycnt_sq += 1

                        if state[row][col] == oppo and state[row + 1][col] == oppo and \
                        state[row][col + 1] == oppo and state[row + 1][col + 1] == oppo:
                            oppcnt_sq += 1
                mymax = max(mymax, mycnt_d1, mycnt_d2, mycnt_sq)
                oppmax = max(oppmax, oppcnt_d1, oppcnt_d2, oppcnt_sq)
        if mymax == oppmax:
            return 0
        elif mymax > oppmax:
            return mymax / 6
        else:
            return (-1) * oppmax / 6

    def Max_Value(self,state,depth):
        #output the best score for Max
        if (game_value(self,state) != 0):
            return self.game_value(self,state) 
        
        elif (depth <= 4):
            return self.heuristic_game_value(self,state)
        
        else:
            alpha = float('-Inf')
            for s in succ(self,state):
                alpha = max(alpha,Min_Value(s,depth + 1))
            return alpha
        
    
    def Min_Value(self,state,depth):
        #output the best score for Min
        if (self.game_value(state) != 0):
            return self.game_value(state) 
        
        elif (depth <= 4):
            return self.heuristic_game_value(state)
        
        else:
            beta = float('Inf')
            for s in self.succ(state):
                beta = min(alpha,self.Max_Value(s,depth + 1))
            return beta        
    
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                        return 1 if state[i][col]==self.my_piece else -1
        # Check \ diagonal wins
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ' and i <= 1 and j <= 1:
                    if (state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3]):
                        return 1 if state[i][j] == self.my_piece else -1

        # Check / diagonal wins
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ' and i >= 3 and j <= 1:
                    if (state[i][j] == state[i - 1][j + 1] == state[i - 2][j + 2] == state[i - 3][j + 3]):
                        return 1 if state[i][j] == self.my_piece else -1

        # Check box win
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i][j+1] == state[i+1][j+1]:
                    return 1 if state[i][j] == self.my_piece else -1       

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
