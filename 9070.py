# -*- coding: utf-8 -*-

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, sql
# for the sys.exit() method call
import sys
# import the Pygame libraries
import pygame
from pygame.locals import *

# import some useful libraries
import pandas as pd
import numpy as np 
from pyecharts import Map
import time
import datetime

# set the DB name, table, and table data to 'None'
db_name = "COVID-19" #need to modify based on the name of local database
Date = None
# initialize the output with None
MostConfirm_return = None
WorldDistribution_return = None

#setting for postgreSQL
#change these globals (user name and user password) to match the settings
user_name = "postgres" #the username for accessing postgreSQL
user_pass = "" #the password for accessing postgreSQL

# create a class for the buttons and labels
class Button():

    # empty list for button registry
    registry = []

    # selected button (will have outline rect)
    selected = None

    # pygame RGBA colors
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    red = (255, 69, 0, 255)
    #blue = (0,191,255,255)
    transp= (0,0,0,0)

    # default font color for buttons/labels is black
    def __init__(self, name, loc, color=black):

        # add button to registry
        self.registry.append(self)

        # paramater attributes
        self.name = name
        self.loc = loc
        self.color = color

        # text attr for button
        self.text = ""

        # size of button changes depending on length of text
        self.size = (int(len(self.text)*200), 200)

        # font.render(text, antialias, color, background=None) -> Surface
        self.font = font.render (
            self.name + " " + self.text, # display text
            True, # antialias on
            self.color, # font color
            #self.transp # background color
        )

        # rect for button
        self.rect = self.font.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

# function that connects to Postgres
def connect_postgres(db):

    # connect to PostgreSQL
    print ("\nconnecting to PostgreSQL")
    try:
        conn = connect (
            dbname = db,
            user = user_name,
            host = "localhost",
            password = user_pass
        )
    except Exception as err:
        print ("PostgreSQL Connect() ERROR:", err)
        conn = None

    # return the connection object
    return conn

def return_MostConfirm_records(conn):
    if Date== None or Date== '':
        return None
    SQLquery='SELECT countryname,confirmedcases FROM OneCountryConfirmed WHERE date =\''\
    +Date+'\'order by ConfirmedCases desc limit 1;'

    print(SQLquery)
    # instantiate a new cursor object
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        MostConfirm_return = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        MostConfirm_return = None

    return MostConfirm_return

def return_WorldDistribution(conn):
    if Date== None or Date== '':
        return None
    SQLquery='SELECT * FROM KeyCountryConfirmed WHERE Date=\''+Date+'\';'

    print(SQLquery)
    # instantiate a new cursor object
    cursor = conn.cursor()

    # (use sql.SQL() to prevent SQL injection attack)
    sql_object = sql.SQL(
        # pass SQL statement to sql.SQL() method
        SQLquery
    )

    try:
        # use the execute() method to put table data into cursor obj
        cursor.execute( sql_object )

        # use the fetchall() method to return a list of all the data
        WorldDistribution_return = cursor.fetchall()

        # close cursor objects to avoid memory leaks
        cursor.close()
    except Exception as err:

        # print psycopg2 error and set table data to None
        print ("PostgreSQL psycopg2 cursor.execute() ERROR:", err)
        WorldDistribution_return = None

    return WorldDistribution_return


"""
PYGAME STARTS HERE
"""

# initialize the pygame window
pygame.init()
pygame.display.set_mode((1000, 500))

# change the caption/title for the Pygame app
pygame.display.set_caption("2020/2021 DST2 Mini-Project",
                           "2020/2021 DST2 Mini-Project")

# get the OS screen/monitor resolution
max_width = pygame.display.Info().current_w
max_height = pygame.display.Info().current_h

# create a pygame resizable screen
screen = pygame.display.set_mode(
    (int(max_width*0.55), int(max_height*0.6)),
    HWSURFACE | DOUBLEBUF| RESIZABLE
)

# calculate an int for the font size
font_size = int(max_width / 50)

try:
    font = pygame.font.SysFont('corbel', font_size)
except Exception as err:
    print ("pygame.font ERROR:", err)
    font = pygame.font.SysFont('Arial', font_size)

# Should set to working directory
bgimage='background1.jpg'
# Set background
background = pygame.image.load(bgimage)

# create buttons for PostgreSQL database and table
Date_button = Button("Date:", (10, 10))

# default Postgres connection is 'None'
connection = None

# begin the pygame loop
app_running = True
while app_running == True:

    # reset the screen
    screen.blit(background,(0,0))

    # set the clock FPS for app
    clock = pygame.time.Clock()

    # iterate over the pygame events
    for event in pygame.event.get():

        # user clicks the quit button on app window
        if event.type == QUIT:
            app_running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            quit()

        # user presses a key on keyboard
        if event.type == KEYDOWN:

            if Button.selected != None:

                # get the selected button
                b = Button.selected

                # user presses the return key
                if event.key == K_RETURN:
                    MostConfirm_return = None
                    WorldDistribution_return = None

                    # check if the selected button is the actor name
                    if "Date" in b.name:
                        Date = b.text

                    connection = connect_postgres( db_name )
                    MostConfirm_return = \
                    return_MostConfirm_records( connection )
                    WorldDistribution_return =\
                    return_WorldDistribution( connection )

                    # reset the button selected
                    Button.selected = None
                    # Generate the map
                    value=list(WorldDistribution_return[0])
                    del(value[0])
                    attr = ["China","United States","United Kingdom",
                            "Italy","France","Germany","Spain","Iran"]    
                    map0 = Map("The Number of People Infected in "+Date, 
                               width=1200, height=600)
                    map0.add("World Map", attr, value, maptype="world", 
                             is_visualmap=True, visual_text_color='#000')
                    map0.render(path="world.html")
                    print(MostConfirm_return)

                else:
                    # get the key pressed
                    key_press = pygame.key.get_pressed()

                    # iterate over the keypresses
                    for keys in range(255):
                        if key_press[keys]:
                            if keys == 8: # backspace
                                b.text = b.text[:-1]
                            else:
                                # convert key to unicode string
                                b.text += event.unicode
                                print ("KEYPRESS:", event.unicode)

                # append the button text to button font object
                color = Button.black
                b.font = font.render(b.name + " " + b.text, True, color)

        # check for mouse button down events
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            print ("\nMOUSE CLICK:", event)

            # iterate over the button registry list
            for b in Button.registry:

                # check if the mouse click collided with button
                if b.rect.collidepoint(event.pos) == 1:
                    # store button object under selected attr
                    Button.selected = b

    # iterate over the button registry list
    for b in Button.registry:

        # blit the button's font to screen
        screen.blit(b.font, b.rect)

        # check if the button has been clicked by user
        if Button.selected == b:

            # blit an outline around button if selected
            rect_pos = \
            (b.rect.x-5, b.rect.y-5, b.rect.width+10, b.rect.height+10)
            pygame.draw.rect(screen, Button.white, rect_pos, 3) # width 3 pixels

    # blit the PostgreSQL information using pygame's font.render() method
    if Date == None:

        # blit instruction messages
        blit_text = "Type the date you are interested in, such as 2020-01-22."
        color = Button.black
        conn_msg = font.render(blit_text, True,color)
        screen.blit(conn_msg, (10, 200))

    else:
        # connection is valid, but MostConfirm doesn't exist
        if connection != None and MostConfirm_return == None:
            blit_text = \
            "The PostgreSQL table does not have the record with this date"
            color = Button.red
            # blit the message to the pygame screen
            conn_msg = font.render(blit_text, True, color)
            screen.blit(conn_msg, (10, 200))

        # connection is valid, but WorldDistribution doesn't exist
        if connection != None and WorldDistribution_return == None:
            blit_text = \
            "The PostgreSQL table does not have the record with this date"
            color = Button.red
            # blit the message to the pygame screen
            conn_msg = font.render(blit_text, True, color)
            screen.blit(conn_msg, (10, 200))

        # connection is invalid
        elif connection == None:
            blit_text = "PostgreSQL connection is invalid."
            color = Button.red
            # blit the message to the pygame screen
            conn_msg = font.render(blit_text, True, color)
            screen.blit(conn_msg, (10, 200))



        # enumerate() the information if PostgreSQL API call successful
        if MostConfirm_return != None:

            # enumerate the list of tuple rows
            for num, row in enumerate(MostConfirm_return):

                # blit the table data to Pygame window
                blit_text="Most cases: "+str(MostConfirm_return[0][0])\
                +"  Number: "+str(MostConfirm_return[0][1])
                color = Button.black
                table_font = font.render(blit_text, True, color)
                screen.blit(table_font, (10, 250 + int(num*50)))

    # set the clock FPS for application
    clock.tick(20)

    # use the flip() method to display text on surface
    pygame.display.flip()
    pygame.display.update()