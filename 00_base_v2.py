from functools import partial
from tkinter import *
import csv
import random


class ChooseRounds:
    def __init__(self):
        # invoke play of 3 rounds for testing purposes
        self.to_play(3)
    
    def to_play(self, num_rounds):
        Play(num_rounds)

        # hide root window
        root.withdraw()
    
class Play:
    
    def __init__(self, how_many):
        self.play_box = Toplevel()

        # if user presses cross at top, closes help and 
        # 'releases ' help button
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))

        # Variables used to wor out statistics, when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # initially set rounds played and rounds won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user score/s and computer score/s
        # used to work out statistics

        user_scores = []
        computer_scores = []

        # get all colours for use in game
        self.all_colours = self.get_all_colours()


        self.quest_frame = Frame(self.play_box, padx = 10, pady = 10)
        self.quest_frame.grid()

        rounds_heading = 'Choose - Round 1 of {}'.format(how_many)
        self.choose_heading = Label(self.quest_frame, text = rounds_heading,\
                                     font = ('Arial', '16', 'bold'))
        self.choose_heading.grid(row = 0)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame, text=  'Start Over',\
                                        command = self.close_play)
        self.start_over_button.grid(row = 0, column= 2)


    
    def close_play(self):
        # reshow root (ie: choose rounds) and end current 
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()



# main routine 
if __name__ == '__main__':
    root = Tk()
    root.title('Color Quest')
    ChooseRounds()
    root.mainloop()
