import csv
import random

# first we need to get the first 50 items \
# from our list, and remove the header

# this gets the list
file = open('00_colour_list_hex_v3.csv', 'r')
all_colours = list(csv.reader(file, delimiter= ','))
file.close()

all_colours.pop(0)
first_50_colours = all_colours[:50]
print('Length : {}'.format(len(first_50_colours)))

# now we need to pick 6 different numbers between 1 and 50 for each round
colours = []

#uses a while loop to get 6 different numbers between 1 - 50
for item in range(0, 3):
    round_colour_list = []
    colour_scores = []

    # get six unique colours
    while len(round_colour_list) < 6:
        # choose item
        chosen_colour = random.choice(first_50_colours)
        index_chosen = first_50_colours.index(chosen_colour)

        # check score is not allready in list
        if chosen_colour[2] not in colour_scores:
            # add  item to rounds list
            round_colour_list.append(chosen_colour)

            # remove item from master list
            first_50_colours.pop(index_chosen)
    
    print('Round Colours:', round_colour_list)
    print('Colour List Length: ', len(first_50_colours))
    print()

    


        
