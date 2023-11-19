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

        instructions = 'Choose one of the colours below. When you choose '\
                        'a colour, the computers choice and the results of '\
                        'the round will be revealed'
        self.instructions_label = Label(self.quest_frame, text = instructions, \
                                        wraplength= 350, justify='left')
        self.instructions_label.grid(row = 1)

        # get colours for buttons first round ...
        button_colours_list = self.get_round_colours()
        print(button_colours_list) # for testing purposes REMOVE later

        # create colour buttons (in choce frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame, \
                                        fg = button_colours_list[item][2],\
                                        bg = button_colours_list[item][0],\
                                        text='{}'.format(button_colours_list[item][0]),\
                                        width = 15,\
                                        command = lambda i = item: self.to_compare(button_colours_list[i][1]))
            self.choice_button.grid(row=item // 3, column= item % 3, padx=5,pady=5)

        #display computer choice (after user has picked a colour)
        self.comp_choice_label = Label(self.quest_frame, \
                                       text = 'Computer choice will appear',\
                                       bg = '#C0C0C0', width = 51)
        self.comp_choice_label.grid(row=3,pady=10)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.round_results_label = Label(self.rounds_frame, text = 'Round Results',\
                                         width=32, bg = '#FFF2CC',\
                                         font=('Arial', 10),\
                                            pady = 5)
        self.round_results_label.grid(row=0,column=0,padx=5)

        self.next_button = Button(self.rounds_frame, text='Next Round',\
                                  fg='#FFFFFF', bg='#0088FC',\
                                  font=('Arial',11,'bold'),\
                                  width = 10,state=DISABLED)
        self.next_button.grid(row=0,column=1)

        #large label to show overall game results
        self.game_results_label = Label(self.quest_frame,\
                                        text='Game Totals: User: - \t Computer:',\
                                        bg='#FFF2CC',padx=10,pady=10,\
                                            font=('Arial','10'),width=42)
        self.game_results_label.grid(row=5,pady=5)


        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons=[
            ['#CC6600','Help','get help'],
            ['#004C99','Statistics','get stats'],
            ['#808080','Start Over','start over']
        ]
        for item in range(0,3):
            self.make_control_button=Button(self.control_frame,\
                                            fg='#FFFFFF',bg=control_buttons[item][0],\
                                            text=control_buttons[item][1],\
                                            width=11,font=('Arial','12','bold'),\
                                            command=lambda i=item:self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0,column=item,padx=5,pady=5)


    # retrive colours from csv file 
    def get_all_colours(self):
        file = open('00_colour_list_hex_v3.csv', 'r')
        var_all_colours = list(csv.reader(file, delimiter = ','))
        file.close()

        # removes first entry in list (the header row)
        var_all_colours.pop(0)
        return var_all_colours
    
    # randomly choose six differemt colours for the buttons
    def get_round_colours(self):
        round_colour_list = []
        color_scores = []

        # get six unique colors 
        while len(round_colour_list) < 6:
            # choose item
            choosen_colour = random.choice(self.all_colours)
            index_chosen = self.all_colours.index(choosen_colour)

            # check if score is not allready in the list
            if choosen_colour[1] not in color_scores:
                # add item to rounds list
                round_colour_list.append(choosen_colour)
                color_scores.append(choosen_colour[1])

                # remove item from the master list
                self.all_colours.pop(index_chosen)
        
        return round_colour_list
    
    def to_compare(self, user_score):
        print('Your score is : {}'.format(user_score))

    def to_do(self,action):
        if action == 'get help':
            self.get_help()
        elif action == 'get stats':
            self.get_stats()
        else:
            self.close_play()
    
    def get_stats(self):
        print('You chose stats')
    
    def get_help(self):
        print('You choose help')
        


    
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
