import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
MAX_TIME_LIMIT = 60
WIDTH, HEIGHT = 1200,800

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

board_matrix=[
              ["First","Second","Third","Fourth","Fifth","Sixth"],
              [200,200,200,200,200,200],
              [400,400,400,400,400,400],
              [600,600,600,600,600,600],
              [800,800,800,800,800,800],
              [1000,1000,1000,1000,1000,1000]
              ]
q={}
def get_questions():
    # fileName = input('Enter Question File Name:')
    fileName = 'qset4_Book'
    df = pd.read_csv(fileName+'.csv',header=0)
    for i,row in enumerate(df['Row']):
            question = str(df["Question"][i])
            answer = str(df["Answer"][i])
            q[(row,df['Col'][i])]={"question":question,"answer":answer}
    for i,cat in enumerate(range(6)):
        board_matrix[0][i]=df['Categories'][i]

get_questions()

class Player(object):
    def __init__(self):
        self.score = 0
        # self.team_name=team_name
        # self.players = players

    def set_score(self,score):
        self.score = score


p1 = Player()
show_question_flag=False
start_flag = False
# team_number = int(input("Number of teams: "))
team_names = []
team_scores = []
already_selected = []

# for i in range(team_number):
#     name=input("Team Name: ")
#     team_names.append(name)
#     team_scores.append(0)

# print(team_names)
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Jeoprady by Pharzan')
clock = pygame.time.Clock()

white = (255,255,255)
grey = (160,160,160)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)

# WIDTH, HEIGHT = 1200,600

class TeamSetupScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.team_count = 2
        self.team_inputs = []
        self.active_input = None
        self.done_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        
    def show(self):
        running = True
        input_boxes = []
        
        while running:
            self.screen.fill(white)
            
            # Title
            title = self.font_large.render("Team Setup", True, blue)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            
            # Team count controls
            count_text = self.font_medium.render("Number of Teams:", True, black)
            self.screen.blit(count_text, (WIDTH // 2 - 200, 150))
            
            minus_button = pygame.Rect(WIDTH // 2 + 50, 150, 50, 50)
            pygame.draw.rect(self.screen, red, minus_button)
            minus_text = self.font_medium.render("-", True, white)
            self.screen.blit(minus_text, (minus_button.x + 20, minus_button.y + 10))
            
            count_display = self.font_medium.render(str(self.team_count), True, black)
            self.screen.blit(count_display, (WIDTH // 2, 150))
            
            plus_button = pygame.Rect(WIDTH // 2 + 150, 150, 50, 50)
            pygame.draw.rect(self.screen, green, plus_button)
            plus_text = self.font_medium.render("+", True, white)
            self.screen.blit(plus_text, (plus_button.x + 20, plus_button.y + 10))
            
            # Team name inputs
            if len(self.team_inputs) != self.team_count:
                self.team_inputs = ["" for _ in range(self.team_count)]
                input_boxes = [pygame.Rect(WIDTH // 2 - 150, 250 + i * 60, 300, 40) for i in range(self.team_count)]
            
            for i, box in enumerate(input_boxes):
                label = self.font_small.render(f"Team {i+1}:", True, black)
                self.screen.blit(label, (box.x - 100, box.y + 10))
                
                color = blue if self.active_input == i else black
                pygame.draw.rect(self.screen, color, box, 2)
                
                text_surface = self.font_small.render(self.team_inputs[i], True, black)
                self.screen.blit(text_surface, (box.x + 5, box.y + 10))
            
            # Done button
            pygame.draw.rect(self.screen, green, self.done_button)
            done_text = self.font_medium.render("Start Game", True, white)
            self.screen.blit(done_text, (self.done_button.x + 20, self.done_button.y + 10))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check team count buttons
                    if minus_button.collidepoint(event.pos) and self.team_count > 1:
                        self.team_count -= 1
                    elif plus_button.collidepoint(event.pos) and self.team_count < 6:
                        self.team_count += 1
                    
                    # Check input boxes
                    self.active_input = None
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            self.active_input = i
                    
                    # Check done button
                    if self.done_button.collidepoint(event.pos):
                        if all(name.strip() != "" for name in self.team_inputs):
                            global team_names, team_scores
                            team_names = self.team_inputs
                            team_scores = [0] * self.team_count
                            return
                
                if event.type == pygame.KEYDOWN and self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        self.team_inputs[self.active_input] = self.team_inputs[self.active_input][:-1]
                    else:
                        if len(self.team_inputs[self.active_input]) < 15:
                            self.team_inputs[self.active_input] += event.unicode
            
            pygame.display.flip()
            clock.tick(30)

class Pane(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 18)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
        self.screen.fill((white))
        self.draw_grid_flag=True
        pygame.display.update()


    def draw_grid(self):
        if self.draw_grid_flag:
            self.screen.fill((white))    
            self.rect = pygame.draw.rect(self.screen, (blue), (0, 0, WIDTH, 100))
            self.draw_grid_flag=False
            self.show_score()
            self.show_selected_box()
        # pygame.display.update()

        cell_pos=WIDTH/6


        for row in range(6):
            cell_pos=WIDTH/6
            for x,header in enumerate(range(6)):
                self.rect = pygame.draw.rect(self.screen, (black), (0, row*100, cell_pos, 100),2)
                cell_pos+=WIDTH/6
                # pygame.display.update()
        pygame.display.update()

    def clear_already_selected(self,col,row):
        pygame.draw.rect(self.screen, (black), (row*(WIDTH/6), col*100, WIDTH/6, 100))
        
    def show_score(self):
        curser=10
        self.rect = pygame.draw.rect(self.screen, (grey), (0,600 , WIDTH, 100))
        for team in team_names:
            self.screen.blit(self.font.render(team, True, (255,0,0)), (curser, 610))
            curser+=WIDTH/6
        curser=10
        for score in team_scores:
            self.screen.blit(self.font.render(str(score), True, (255,0,0)), (curser, 640))
            curser+=WIDTH/6
    def show_selected_box(self):
        self.show_score()
        self.rect = pygame.draw.rect(self.screen, (red), (selected_team_index*(WIDTH/6),600 , WIDTH/6, 100),3)
        self.rect = pygame.draw.rect(self.screen, (red), (selected_team_index*(WIDTH/6),700 , WIDTH/6, 100))
        
    def addText(self,pos,text):
        # print(pos,text)
        x = pos[0]*WIDTH/6+10
        y= 100*pos[1]+35
        color = red
        # print('Y',y)
        if y<100:
            color=yellow
        self.screen.blit(self.font.render(str(text), True, color), (x, y))
        
class Question(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Open Sans', 32)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT+200), 0, 32)
        self.screen.fill((white))
        pygame.display.update()

    def show(self,q):
        # curser=0
        self.rect = pygame.draw.rect(self.screen, (black), (0, 0, WIDTH, HEIGHT))
        sizeX, sizeY = self.font.size(q)
        if (sizeX>WIDTH):
            print("TEXT TOOO LONG!!!")
        print('SHOW QUESTION:',r,c)
        self.screen.blit(self.font.render(q, True, (255,0,0)), (WIDTH/2-(sizeX/2), HEIGHT/2))
        pygame.display.update()

    def show_answer(self,text):
        self.screen.fill((black))
        sizeX, sizeY = self.font.size(text)
        self.screen.blit(self.font.render(str(text), True, (255,0,0)), (WIDTH/2-(sizeX/2), HEIGHT/2))
        self.rect = pygame.draw.rect(self.screen, (green), ((WIDTH/6), 500, WIDTH/6, 100))
        self.rect = pygame.draw.rect(self.screen, (red), (4*(WIDTH/6), 500, WIDTH/6, 100))
        self.rect = pygame.draw.rect(self.screen, (grey), ((WIDTH/2)-(WIDTH/(18*2)), 500, WIDTH/18, 100))
        pygame.display.update()

class Timer(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,800), 0, 32)
        self.font = pygame.font.SysFont('Arial', 32)
        self.timer_x_pos=(WIDTH/2)-(WIDTH/12)
        self.timer_y_pos=WIDTH/6
        self.counter=0
        self.startTime=0
        self.elapsed=0

    def start(self):
        self.startTime = time.perf_counter()

    def show(self):
        self.elapsed = round(time.perf_counter()-self.startTime,1)
        self.rect = pygame.draw.rect(self.screen, (blue), (self.timer_x_pos, 500, self.timer_y_pos, 100))
        self.screen.blit(self.font.render(str(self.elapsed), True, (255,255,0)), (self.timer_x_pos+25,550))
        if self.elapsed >= MAX_TIME_LIMIT:
            pygame.mixer.music.load('buzzer2.wav')
            pygame.mixer.music.play()
            timer.start()

current_selected=[0,0]
team_selected = False
question_time = False
pane1= Pane()
question_screen = Question()
timer = Timer()
grid_drawn_flag = False
selected_team_index=-1
show_timer_flag = False
Running_flag = True

class Cell(object):
    def __init__(self):
        self.X=0
        self.Y=0
        self.text=''
class HomeScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('Arial', 48)
        self.title_text = self.font.render('Welcome to Jeopardy!', True, (0, 0, 255))
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

    def show(self):
        self.screen.fill(white)
        self.screen.blit(self.title_text, (WIDTH // 2 - self.title_text.get_width() // 2, HEIGHT // 3))
        pygame.draw.rect(self.screen, blue, self.start_button)
        start_text = self.font.render("Start", True, white)
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()

    def wait_for_click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return  # Start the game
home_screen = HomeScreen()
home_screen.show()
home_screen.wait_for_click()
team_setup = TeamSetupScreen()
team_setup.show()
while Running_flag:
    click_count=0
    clock.tick(60)
    while not question_time:
        r, c = 0 , 0
        if not grid_drawn_flag:
            pane1.draw_grid()
            for i in range(6):
                for j in range(6):
                    pane1.addText((i,j),board_matrix[j][i])
            grid_drawn_flag=True

        for each_already_selected in already_selected:
            # print(each_already_selected[0],each_already_selected[1])
            pane1.clear_already_selected(each_already_selected[0],each_already_selected[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                print("Quit")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if team_selected:
                    print('Board Time')
                    for col in range(7):
                        if(col*(WIDTH/6)<event.pos[0]<(col+1)*(WIDTH/6)):
                            # print('col',col)
                            c = col
                            for row in range(6):
                                if(row*(HEIGHT/6)<event.pos[1]<(row+1)*(HEIGHT/6)):
                                    r = row
                                    print('Clicked on:',r,c,'SCORE:',board_matrix[r][c])
                                    show_question_flag = True
                                    if (r,c) not in already_selected:
                                        already_selected.append((r,c))
                                        current_selected = [r,c]
                                        question_time = True
                                    else:
                                        print('already selected')
                else:
                    print('First select a team')
                    for col in range(6):
                        if(col*(WIDTH/6)<event.pos[0]<(col+1)*(WIDTH/6) and event.pos[1]>600):
                            # answering_team = teams[col]
                            print('Selected Team:',col, 'Selected Team Name:',team_names[col],'score',team_scores[col])
                            selected_team_index = col
                            pane1.show_selected_box()
                            team_selected = True

            if event.type == pygame.QUIT:
                crashed = True
            # print(event)
        pygame.display.update()
        clock.tick(60)

    while question_time:      
        grid_drawn_flag = False
        if show_timer_flag:
            timer.show()
        if show_question_flag:
            print("Current Selected",current_selected)
            timer.start()
            try:
                question=q[current_selected[0],current_selected[1]]['question']
                print("Question:",q[current_selected[0],current_selected[1]]['question'])
            except:
                print('No Question Found For Position')
            question_screen.show(question)
            show_question_flag = False
            show_timer_flag = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[1]<600:
                    if event.pos[0]>500 and event.pos[0]<700 and show_timer_flag: 
                        print('Timer')
                        timer.start()
                        break
                    click_count+=1
                    # question_screen.show_answer()
                    print(q[r,c]['answer'])
                    question_screen.show_answer(q[r,c]['answer'])
                    show_timer_flag = False
                    print("Selected Question",c,r,"Points:",board_matrix[c][r],'Click Count:',click_count)
                    print("Question Time")
                    if click_count==2:
                        if (event.pos[0]>(WIDTH/6) and event.pos[0]<2*(WIDTH/6)):
                            print ("RIGHTTTTT")
                            team_scores[selected_team_index] = team_scores[selected_team_index]+board_matrix[r][c]
                        elif (event.pos[0]>4*(WIDTH/6) and event.pos[0]<5*(WIDTH/6)):
                            print('WRONGGGG!')
                            team_scores[selected_team_index] = team_scores[selected_team_index]-board_matrix[r][c]
                        print('Second Click:',event.pos[0],event.pos[1])
                        team_selected = False
                        question_time = False
                        pane1.draw_grid_flag = True
                        click_count = 0
                else:
                    print('NEW TEAM SELECT MODE!')
                    for col in range(6):
                        if(col*(WIDTH/6)<event.pos[0]<(col+1)*(WIDTH/6) and event.pos[1]>600):
                            # answering_team = teams[col]
                            print('New Selected Team:',col, 'Selected Team Name:',team_names[col],
                                  'score',team_scores[col],
                                  'Previous selected team score',team_scores[selected_team_index],
                                  'Score:',board_matrix[r][c])
                            team_scores[selected_team_index]=team_scores[selected_team_index]-board_matrix[r][c]
                            selected_team_index = col
                            pane1.show_score()
                            pane1.show_selected_box()
                            timer.start()
        pygame.display.update()
        clock.tick(60)