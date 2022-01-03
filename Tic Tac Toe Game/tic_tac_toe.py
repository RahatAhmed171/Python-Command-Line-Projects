from abc import ABC,abstractmethod

class GameInterface(ABC):
    @abstractmethod
    def quit(self):
        pass
    @abstractmethod
    def start(self):
        pass
class InvalidMoveError(Exception):
    def __init__(self):
        super().__init__("Invalid position. Put correct position")

class Tic_Tac__Toe_Board_System:
    def __init__(self):
        self.board=[[0,0,0],[0,0,0],[0,0,0]]
        self.position_filled=[]
    
    def display_board(self):
        for i in range(3):
            print(self.board[i])
            print("\t")
    
    def check_if_a_position_valid(self,x,y):
        if int(x)>2 or int(y)>2:
            raise InvalidMoveError()
        position=x+y
        for i in range(len(self.position_filled)):
            if position==self.position_filled[i]:
                raise InvalidMoveError()


    def check_if_three_consecutive_spots_are_similar(self,position):
        positions={
            '00':[[0,0],[0,1,0,2],[1,1,2,2],[1,0,2,0]],
            '01':[[0,1],[0,0,0,2],[1,1,2,1]],
            '02':[[0,2],[0,0,0,1],[1,2,2,2]],
            '10':[[1,0],[0,0,2,0],[1,1,1,2]],
            '11':[[1,1],[0,1,2,1],[1,0,1,2],[0,0,2,2],[0,2,2,0]],
            '12':[[1,2],[0,2,2,2],[1,0,1,1]],
            '20':[[2,0],[0,0,1,0],[2,1,2,2],[0,2,1,1]],
            '21':[[2,1],[2,0,2,2],[0,1,1,1]],
            '22':[[2,2],[2,0,2,1],[0,2,1,2],[0,0,1,1]],
        }
        all_position=positions[position]
        cposition=all_position[0]
        
        for i in all_position[1:]:
            if self.board[cposition[0]][cposition[1]]==self.board[i[0]][i[1]] and self.board[cposition[0]][cposition[1]]==self.board[i[2]][i[3]]:
                return True




class Players:
    def __init__(self):
        self.count=1
        self.next_turn='Player One'
        self.symbol='5'
        self.current_player="Player One"
        
    
    def turn_of_a_player(self):
       
        if self.count%2==0:
            self.symbol=8
            self.current_player="Player Two"
            self.count=self.count+1
            self.next_turn="Player One"
            return self.symbol
        else:
            self.symbol=5
            self.current_player="Player One"
            self.count=self.count+1
            self.next_turn="Player Two"
            return self.symbol
    
    











class Tic_Tac_Toe_Game:
    def __init__(self,players):
        self.board_system=Tic_Tac__Toe_Board_System()
        self.the_players=players
        
        self.no_of_moves=0

        


    

    def put_a_symbol_on_the_board(self,x,y):

            self.board_system.check_if_a_position_valid(x,y)
            symbol=self.the_players.turn_of_a_player()
            position=x+y
            self.board_system.board[int(x)][int(y)]=symbol
            self.board_system.position_filled.append(position)
            self.no_of_moves=self.no_of_moves+1
            if self.no_of_moves>=5:
                self.check_the_winner(position)
                

            self.check_if_game_tied()
        

    def check_if_game_tied(self):
        if self.the_players.count==9:
            print("Game Tied")
            exit()

    def check_the_winner(self,position):
        is_similar=self.board_system.check_if_three_consecutive_spots_are_similar(position)
        if is_similar:
            self.board_system.display_board()
            print(f'{self.the_players.current_player} has won the game')
            exit()
        else:
            return
            
        



        

   




class CommandLineInterface(GameInterface):
    def __init__(self):
        self.tic_tac_toe_game=Tic_Tac_Toe_Game(Players())
        

    def quit(self):
        exit()
    
    def player_make_a_move(self):
        print(''' To make a move put the x and y coordinates of a position in the board''')
        print(f'{self.tic_tac_toe_game.the_players.next_turn} will make a move now!')
        try:
            position_x=input('Enter the x coordinate:')
            position_y=input('Enter the y coordinate: ')
            self.tic_tac_toe_game.put_a_symbol_on_the_board(position_x,position_y)
            

        except InvalidMoveError as e:
            print(e)   
        except Exception as e:
            print("Some error has occured")
    
    def start(self):
        while True:
            self.tic_tac_toe_game.board_system.display_board()
            self.player_make_a_move()

    def menu_options(self):
        
        print(''' Welcome to Tic Tac Toe game.
Press 1 to start the game,
Press 0 to quit.       
        ''')
        choice=input("Enter your choice: ")
        if choice=='1':
            self.start()
        elif choice=='0':
            self.quit()
        else:
            print("Invalid choice.")
    

def main():
    CommandLineInterface().menu_options()


if __name__=='__main__':
    main()

    

