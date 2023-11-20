from functools import partial
from tkinter import *
import csv
import random


class ChooseRounds:
    def __init__(self):
        button_fg = '#FFFFFF'
        button_font = ('Arial', '13', 'bold')

        #set up GUI Frame
        self.intro_frame = Frame(padx = 10, pady = 10)
        self.intro_frame.grid()
        
        # heading and brief instructions
        self.intro_heading_label = Label(self.intro_frame, text= 'Color Quest', font = ('Arial', '16','bold'))
        self.intro_heading_label.grid(row = 0)

        choose_instructions_txt = 'In each round you will be given '\
                                    'six different colors to choose '\
                                    'from. Pick a color and see if '\
                                    'you can beat the computers '\
                                    'score\n\n'\
                                    'To begin choose how many rounds '\
                                    'youd like to play'
        self.choose_instructions_label = Label(self.intro_frame, text= choose_instructions_txt, wraplength= 300, justify= 'left')
        self.choose_instructions_label.grid(row = 1)

        #rounds buttons
        self.how_many_frame = Frame(self.intro_frame)
        self.how_many_frame.grid(row=2)

        #list to set up rounds button. First Item 
        # in each sublist is the background color,
        # second item is the number of rounds

        btn_color_value = [
            ['#CC0000', 3], ['#009900', 5], ['#000099', 10]
        ]

        # for loop sets up all of the rounds buttons
        for item in range(0, 3):
            self.rounds_button = Button(self.how_many_frame, fg = button_fg, bg = btn_color_value[item][0], \
                                         text = '{} Rounds'.format(btn_color_value[item][1]),\
                                         font = button_font, width = 10,\
                                         command = lambda i = item: self.to_play(btn_color_value[i][1]))
        
            self.rounds_button.grid(row = 0,column=item, padx = 5, pady = 5)
    
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

        self.user_scores = []
        self.computer_scores = []

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
        self.button_colours_list = self.get_round_colours()
        print(self.button_colours_list) # for testing purposes REMOVE later

        # create colour buttons (in choce frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        # list to hold references for coloured buttons
        # so that they can be configured for new rounds
        self.choice_button_ref = []


        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame, \
                                        width = 15,\
                                        command = lambda i = item: self.to_compare(self.button_colours_list[i]))
            # add button to reference list for later config
            self.choice_button_ref.append(self.choice_button)
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
                                         font=('Arial', '10'),\
                                            pady = 5)
        self.round_results_label.grid(row=0,column=0,padx=5)

        self.next_button = Button(self.rounds_frame, text='Next Round',\
                                  fg='#FFFFFF', bg='#0088FC',\
                                  font=('Arial','11','bold'),\
                                  width = 10,state=DISABLED,command=lambda: self.new_round())
        self.next_button.grid(row=0,column=1)

        # at start get 'new round'

        self.new_round()

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

        self.control_button_ref = []

        for item in range(0,3):
            self.make_control_button=Button(self.control_frame,\
                                            fg='#FFFFFF',bg=control_buttons[item][0],\
                                            text=control_buttons[item][1],\
                                            width=11,font=('Arial','12','bold'),\
                                            command=lambda i=item:self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0,column=item,padx=5,pady=5)
            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        # disable stats button in first round because their is no stats to see. 
        self.to_stats_btn.config(state=DISABLED)


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
    
    def new_round(self):

        # disable next button (reenable it at the end of round)
        self.next_button.config(state=DISABLED)

        # need to set comp choice label back to its standard colour
        self.comp_choice_label.config(text= 'Computer Choice will appear here.', bg= '#C0C0C0')

        # empty button list so we can get new colours
        self.button_colours_list.clear()

        #get new colours for buttons
        self.button_colours_list = self.get_round_colours()

        # set button bg, fg, and text
        count = 0
        for item in self.choice_button_ref:
            item['fg'] = self.button_colours_list[count][2]
            item['bg'] = self.button_colours_list[count][0]
            item['text'] = self.button_colours_list[count][0]
            item['state'] = NORMAL

            count+=1
        
        # retrieve number of rounds wanted / played and update heading
        how_many=self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = 'Choose - Round {} of {}'.format(current_round + 1, how_many)
        self.choose_heading.config(text = new_heading)

    def to_compare(self, user_choice):
        
        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1 
        self.rounds_played.set(current_round)

        # enable stats button
        self.to_stats_btn.config(state=NORMAL)

        # deactivate colour buttons
        for item in self.choice_button_ref:
            item.config(state=DISABLED)
        
        # set up background colours
        win_colour = '#D5E8D4'
        lose_colour= '#F8CECC'

        # retrieve user score, make it into an interger and add to list for stats
        user_score_current = int(user_choice[1])
        self.user_scores.append(user_score_current)

        # remove user choice from button colour list
        to_remove = self.button_colours_list.index(user_choice)
        self.button_colours_list.pop(to_remove)

        # get computer choice and add to list for stats 
        # when getting score, change it to an interger before 
        # appending
        comp_choice = random.choice(self.button_colours_list)
        comp_score_current = int(comp_choice[1])

        self.computer_scores.append(comp_score_current)

        comp_annouce = 'the computer choose {}'.format(comp_choice[0])

        self.comp_choice_label.config(text=comp_annouce,bg=comp_choice[0],fg=comp_choice[2])

        # get colours and show results 
        if user_score_current > comp_score_current:
            round_results_bg = win_colour
        else:
            round_results_bg = lose_colour
        
        rounds_outcome_txt = 'Round {}: User {} \tComputer: {}'.format(current_round,user_score_current,comp_score_current)

        self.round_results_label.config(bg= round_results_bg, text = rounds_outcome_txt)

        # get total scores for user and computer
        user_total = sum(self.user_scores)
        comp_total = sum(self.computer_scores)

        if user_total > comp_total:
            self.game_results_label.config(bg = win_colour)
            status = 'You win!'
        else:
            self.game_results_label.config(bg = lose_colour)
            status = 'You lose!'
        
        game_outcome_txt = 'Total Score: User {} \tComputer: {}'.format(user_total, comp_total)
        self.game_results_label.config(text=game_outcome_txt)

        # if game is over, disable all buttons amd change text of 'next'
        # to either 'You win', or 'You lose' and disable all buttons

        if current_round == how_many:
            # change 'next ' button to show overall
            # win loss result and disable it
            self.next_button.config(state = DISABLED, text=status)

            # update 'start over button'
            start_over_button = self.control_button_ref[2]
            start_over_button['text'] = 'Play again'
            start_over_button['bg'] = '#C0C0C0'

            # change all colour button background to light grey
            for item in self.choice_button_ref:
                item['bg'] = '#C0C0C0'
        
        else:
            #enables next round button and update heading
            self.next_button.config(state=NORMAL)


    def to_do(self,action):
        if action == 'get help':
            Help(self)
        elif action == 'get stats':
            DisplayStats(self,self.user_scores,self.computer_scores)
        else:
            self.close_play()
    

    def close_play(self):
        # reshow root (ie: choose rounds) and end current 
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

class Help:
    def __init__(self, partner):
        self.help_box = Toplevel()
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help))

        partner.to_help_btn.config(state=DISABLED)

        # set up some color variables
        colour_bg = '#FFE6CC'

        self.help_frame = Frame(self.help_box, padx = 10, pady = 10, bg = colour_bg)
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame, text = 'Help Page', fg= '#000000',\
                                  bg = colour_bg, font = ('Arial', '16', 'bold'),\
                                    justify='left')
        self.help_heading.grid(row=0, padx=5,pady=5)

        help_text = 'Your goal in this game is to beat the computer and you have an advantage - you get to choose your colour first. The points are associated with the colours HEX code. The Higher the value of your colour the higher the greater your score.\n\nTo see your statistics, click on the statistics button. Win the game by scoring more then the computer overall. Dont be discouraged if you dont win every round, its your overall score that counts.\n\nGood Luck! Choose Carefully :)'

        self.help_info = Label(self.help_frame, fg='#000000', bg=colour_bg,text=help_text,font=('Arial','11'),wraplength=350,justify='left')
        self.help_info.grid(row=1,padx=5,pady=5)

        #dissmiss button
        self.help_dismiss = Button(self.help_frame,fg='#FFFFFF',bg='#CC6600',text='Dismiss',font=('Arial','14'),command=lambda:self.close_help(partner))
        self.help_dismiss.grid(row=2,padx=5,pady=5)

    

    def close_help(self,partner):
        partner.to_help_btn.config(state=NORMAL)
        
        self.help_box.destroy()
    


class DisplayStats:
    def __init__(self, partner, user_scores, computer_scores):
        self.stats_box = Toplevel()
        # setup dialouge box and background colour

        stats_bg_colour = '#DAE8FC'
        # disable help button
        partner.to_stats_btn.config(state=DISABLED)

        # if user press cross at top closes stats
        # releases stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,height=200,bg=stats_bg_colour)
        self.stats_frame.grid()

        self.stats_heading_label = Label(self.stats_frame,text='Statistics',font=('Arial','14','bold'),bg=stats_bg_colour)
        self.stats_heading_label.grid(row=0)

        stats_text = 'Here are your game statistics.'
        self.stats_text_label = Label(self.stats_frame,text=stats_text,justify='left',bg=stats_bg_colour)
        self.stats_text_label.grid(row=1,padx=10)

        self.data_frame = Frame(self.stats_frame,bg=stats_bg_colour,borderwidth=1,relief='solid')
        self.data_frame.grid(row=2,padx=10,pady=10)

        # get stats for user and computer
        self.user_stats = self.get_stats(user_scores,'User')
        self.comp_stats = self.get_stats(computer_scores,'Computer')

        # background formatting for heading odd and even rows
        head_back = '#FFFFFF'
        odd_rows = '#C9D6E8'
        even_rows = stats_bg_colour

        row_names=['','Total','Best Score','Worst Score','Average Score']
        row_formats=[head_back,odd_rows,even_rows,odd_rows,even_rows]
        # data for labels (one label/sublist)
        all_labels=[]
        count=0
        for item in range(0,len(self.user_stats)):
            all_labels.append([row_names[item], row_formats[count]])
            all_labels.append([self.user_stats[item],row_formats[count]])
            all_labels.append([self.comp_stats[item],row_formats[count]])
            count+=1

        # create labels based on list above
        for item in range(0, len(all_labels)):
            self.data_label = Label(self.data_frame,text=all_labels[item][0],bg=all_labels[item][1],width='10',height='2',padx=5)
            self.data_label.grid(row=item//3,column=item%3,padx=0,pady=0)
        
        self.stats_dismiss = Button(self.stats_frame,fg='#FFFFFF',bg='#CC6600',text='Dismiss',font=('Arial','14'),command=lambda:self.close_stats(partner))
        self.stats_dismiss.grid(row=3,padx=5,pady=5)
        
        


        


    @staticmethod
    def get_stats(score_list, entitiy):
        total_score = sum(score_list)
        best_score = max(score_list)
        worst_score = min(score_list)
        average = total_score / len(score_list)

        # set average todisplay 1 dp
        average = '{:.1f}'.format(average)
        return [entitiy, total_score, best_score, worst_score, average]
    
    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()












# main routine 
if __name__ == '__main__':
    root = Tk()
    root.title('Color Quest')
    ChooseRounds()
    root.mainloop()
