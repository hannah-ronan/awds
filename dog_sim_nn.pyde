
# create empty variables to hold the image assets
steak_img = None
water_img = None
dog1_img = None
dog2_img = None
dog3_img = None
dog4_img = None
dog1_f_img = None
dog2_f_img = None
dog3_f_img = None
dog4_f_img = None
pointer_img = None
menu_bg_img = None

#Create some example items
# dogs[i] = ["image name", horizontal grid position, vertical grid position, gender(0=male)]
# waters[i] = [horizontal grid position, vertical grid position]
# steaks[i] = [horizontal grid position, vertical grid position]

data = []

closest_mate = 0
closest_water = 0
closest_steak = 0
current_dog = 0

time = 0

maxw1 = 3
maxw2 = 3
maxw3 = 3
maxw4 = 3
maxw5 = 3
maxb = 3

minw1 = -3
minw2 = -3
minw3 = -3
minw4 = -3
minw5 = -3
minb = -3

gen = 0

frame_rate = 4

number_of_games = 200

number_of_gens = 100

starve_rate = 0.5

top_scores = []

mode = "setup"

player = "NN"

def gen_ended():
    global mode
    top_score = natural_selection()
    background(255,157,157)
    text ("generation \t    ended\n highest score:\t", 350,250)
    text (gen,400,230)
    text (top_score,520 ,270)
    text ("press x to start a new generation", 350,400)
    print top_scores
    if gen<number_of_gens:
        mode = "setup done"
        create_data()

def natural_selection():
    global maxw1,maxw2,maxw3,maxw4,maxw5,maxb, minw1,minw2,minw3,minw4,minw5,minb, top_scores
    scores = []

    for game_index in range (number_of_games):
        scores.append([game_index, data[game_index][4][0]])
    scores = sorted(scores, key = lambda x: x[1], reverse = True)
    top_scores.append ([gen, scores[0][1]])

    w1s = []
    w2s = []
    w3s = []
    w4s = []
    w5s = []
    bs = []
    if number_of_games>3:
        for index in range (3):
            w1s.append(data[scores[index][0]][0][5])
            w2s.append(data[scores[index][0]][0][6])
            w3s.append(data[scores[index][0]][0][7])
            w4s.append(data[scores[index][0]][0][8])
            w5s.append(data[scores[index][0]][0][9])
            bs.append(data[scores[index][0]][0][10])
    w1s.sort()
    w2s.sort()
    w3s.sort()
    w4s.sort()
    w5s.sort()
    bs.sort()
    
    maxw1 = w1s[2]
    maxw2 = w2s[2]
    maxw3 = w3s[2]
    maxw4 = w4s[2]
    maxw5 = w5s[2]
    maxb = bs[2]
    
    minw1 = w1s[0]
    minw2 = w2s[0]
    minw3 = w3s[0]
    minw4 = w4s[0]
    minw5 = w5s[0]
    minb = bs[0]
    
    return scores[0][1]
            
        
    
    
        


def create_data():
    global data, gen
    data = []
    gen +=1
    for i in range (number_of_games):
        # [
           #[
            #[fd,h,wd,t,md,w1,w2,w3,w4,w5,b],
            #[
            # [image name, horizontal grid position, vertical grid position, gender]
            #],
            #[
            # [horizontal grid position, vertical grid position]
            #],
            #[
            # [horizontal grid position, vertical grid position]
            #],
            #[score],
            #[target type, target index],
            #[status(1=alive)],
            #[cod]
           # ]
         #  ]
        #character dog x position = data[game_index][1][0][1]
        #character dog y position = data[game_index][1][0][2]

        game_setup(i)

        
def generate_weights(game_index, maxw1,minw1,maxw2,minw2,maxw3,minw3,maxw4,minw4,maxw5,minw5,maxb,minb):
    w1 = random(minw1,maxw1)
    w2 = random(minw2,maxw2)
    w3 = random(minw3,maxw3)
    w4 = random(minw4,maxw4)
    w5 = random(minw5,maxw5)
    b = random(minb,maxb)
    data[game_index][0][5] = w1
    data[game_index][0][6] = w2
    data[game_index][0][7] = w3
    data[game_index][0][8] = w4
    data[game_index][0][9] = w5
    data[game_index][0][10] = b

def sigmoid(x):
    return 1/(1+exp(-x))

def choose_target(game_index):
    fd = data[game_index][0][0]
    h = data[game_index][0][1]
    wd = data[game_index][0][2]
    t = data[game_index][0][3]
    md = data[game_index][0][4]
    w1 = data[game_index][0][5]
    w2 = data[game_index][0][6]
    w3 = data[game_index][0][7]
    w4 = data[game_index][0][8]
    w5 = data[game_index][0][9]
    b = data[game_index][0][10]
    z = fd*w1 + h*w2 + wd*w3 + t*w4 + md*w5 + b
    target_value = sigmoid(z)

    if 0.33>=target_value>0:

        data[game_index][5] = [3,closest_steak]
    elif 0.66>=target_value>0.33:

        data[game_index][5] = [2,closest_water]
    elif 1>=target_value>0.66:

        data[game_index][5] = [1,closest_mate]
    
    


        
def game_setup(game_index):
    global time, mode, current_dog, maxw1,minw1,maxw2,minw2,maxw3,minw3,maxw4,minw4,maxw5,minw5,maxb,minb
    data.append([])
    for i in range (8):
        data[game_index].append([])
    for i in range (11):
        data[game_index][0].append(0)
    data[game_index][4]= [0]
    data[game_index][5]=[0]
    data[game_index][6]=[1]
    data[game_index][7]=[""]
    time = 0
    check_items(game_index)
    rand = int(random(1,3))
    if rand == 1:
        for i in range (2):
            item_create(0,1,game_index)
            item_create(0,0,game_index)
    else:
        for i in range (2):
            item_create(0,0,game_index)
            item_create(0,1,game_index)
    current_dog = int(random(number_of_games))
    generate_weights(game_index, maxw1,minw1,maxw2,minw2,maxw3,minw3,maxw4,minw4,maxw5,minw5,maxb,minb)
    get_distances(game_index)
    choose_target(game_index)
    mode = "running"

    




def get_distances(game_index):
    global closest_mate, closest_steak, closest_water, data
    water_dist = []
    steak_dist = []
    mate_dist = []
    closest_mate = 0
    closest_steak = 0
    closest_water = 0
    
    for i in range (1,len(data[game_index][1])):
        if data[game_index][1][i][3] != data[game_index][1][0][3]:
            x_dist = abs(data[game_index][1][i][1] - data[game_index][1][0][1])
            y_dist = abs(data[game_index][1][i][2] - data[game_index][1][0][2])
            mate_dist.append([i,x_dist+y_dist])
    mate_dist = sorted(mate_dist, key = lambda x: x[1])
    
    if len(mate_dist) != 0:
        data[game_index][0][4] = mate_dist[0][1]
        closest_mate = mate_dist[0][0]
    
    for i in range (len(data[game_index][2])):
        x_dist = abs(data[game_index][2][i][0] - data[game_index][1][0][1])
        y_dist = abs(data[game_index][2][i][1] - data[game_index][1][0][2])
        water_dist.append([i,x_dist+y_dist])
    water_dist = sorted(water_dist, key = lambda x: x[1])
    data[game_index][0][2] = water_dist[0][1]
    closest_water = water_dist[0][0]

    for i in range (len(data[game_index][3])):
        x_dist = abs(data[game_index][3][i][0] - data[game_index][1][0][1])
        y_dist = abs(data[game_index][3][i][1] - data[game_index][1][0][2])
        steak_dist.append([i,x_dist+y_dist])
    steak_dist = sorted(steak_dist, key = lambda x: x[1])
    data[game_index][0][0] = steak_dist[0][1]
    closest_steak = steak_dist[0][0]

    
    if water_dist[0][1] == 0:
        del data[game_index][2][closest_water]
        data[game_index][0][3]-= 4*starve_rate
        data[game_index][4][0] += 1
    if steak_dist[0][1] == 0:
        del data[game_index][3][closest_steak]
        data[game_index][4][0] += 1
        data[game_index][0][1] -= 4*starve_rate
    
    if len(mate_dist) != 0:
        if mate_dist[0][1] == 0:
            del data[game_index][1][closest_mate]
            dog_multiply(game_index)
            data[game_index][4][0] += 2
    

def draw_food(food_type,food_index, game_index):
    if food_type == 0:
        image (water_img,data[game_index][2][food_index][0]*50,data[game_index][2][food_index][1]*50)
    elif food_type == 1:
        image (steak_img,data[game_index][3][food_index][0]*50,data[game_index][3][food_index][1]*50 )
        
def check_items(game_index):
    while len(data[game_index][2])<3:
        item_create(1,2,game_index)
    while len(data[game_index][3])<3:
        item_create(2,2,game_index)

def dog_multiply(game_index):
    global score
    data[game_index][4][0] += 2
    n = int(random(1,4))
    for i in range (n):
        item_create (0,2,game_index)
        
def seek_target(item_type, index, game_index):   #seek_target(data[game_index][5][0],data[game_index][5][1],game_index) 
    global data
  
    x_move = 0
    y_move = 0
    if item_type == 1:
        x_index = 1
        y_index = 2
    else:
        x_index = 0
        y_index = 1
    if (data[game_index][item_type][index][x_index]-data[game_index][1][0][1])>0:
        x_move = 1
    elif(data[game_index][item_type][index][x_index]-data[game_index][1][0][1])<0:
        x_move = -1
    else:
        x_move = 0
        if (data[game_index][item_type][index][y_index]-data[game_index][1][0][2])>0:
            y_move = 1
        elif (data[game_index][item_type][index][y_index]-data[game_index][1][0][2])<0:
            y_move = -1
        else:
            y_move = 0
            if item_type == 1:
                
                dog_multiply(game_index)
            else:
                del data[game_index][item_type][index]
    dog_move(0,x_move,y_move, game_index)

def item_create(item_type, special, game_index):
    global data
    used_coords = []
    for i in range (len(data[game_index][1])):
        coord = [data[game_index][1][i][1],data[game_index][1][i][2]]
        used_coords.append(coord)
    for i in range (len(data[game_index][2])):
        coord = [data[game_index][2][i][0],data[game_index][2][i][1]]
        used_coords.append(coord)
    for i in range (len(data[game_index][3])):
        coord = [data[game_index][3][i][0],data[game_index][3][i][1]]
        used_coords.append(coord)

    rand_x = int(random(0,10))
    rand_y = int(random(0,10))

    status = "looking"
    
    while status == "looking":
        coord = [rand_x,rand_y]
        if coord not in used_coords :
            status = "found"
        elif len(used_coords) == 100: 
            print "no more spaces available"
            status = "done"
        else:
            rand_x = int(random(0,10))
            rand_y = int(random(0,10))

    if item_type == 0: 
        if special == 0:
            rand_colour = int(random(0,4))
            if rand_colour == 0:
                colour = "dog1_img"
                gender = 0
            elif rand_colour == 1:
                colour = "dog2_img"
                gender = 0
            elif rand_colour == 2:
                colour = "dog3_img"
                gender = 0
            elif rand_colour == 3:
                colour = "dog4_img"
                gender = 0
        
        elif special ==1:
            rand_colour = int(random(0,4))
            if rand_colour == 0:
                colour = "dog1_f_img"
                gender = 1
            elif rand_colour == 1:
                colour = "dog2_f_img"
                gender = 1
            elif rand_colour == 2:
                colour = "dog3_f_img"
                gender = 1
            elif rand_colour == 3:
                colour = "dog4_f_img"
                gender = 1
        
        elif special == 2:
            rand_colour = int(random(0,8))
            if rand_colour == 0:
                colour = "dog1_img"
                gender = 0
            elif rand_colour == 1:
                colour = "dog2_img"
                gender = 0
            elif rand_colour == 2:
                colour = "dog3_img"
                gender = 0
            elif rand_colour == 3:
                colour = "dog4_img"
                gender = 0
            elif rand_colour == 4:
                colour = "dog1_f_img"
                gender = 1
            elif rand_colour == 5:
                colour = "dog2_f_img"
                gender = 1
            elif rand_colour == 6:
                colour = "dog3_f_img"
                gender = 1
            elif rand_colour == 7:
                colour = "dog4_f_img"
                gender = 1
        
        data[game_index][1].append([colour, rand_x,rand_y,gender])

    elif item_type == 1:
        data[game_index][2].append([rand_x,rand_y])
    elif item_type == 2:
        data[game_index][3].append([rand_x,rand_y])



def dog_show(dog_index,game_index): 

    if dog_index == 0:
        image (pointer_img, data[game_index][1][0][1]*50,data[game_index][1][0][2]*50)
    if data[game_index][1][dog_index][0]== "dog1_f_img":
        image (dog1_f_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
    elif data[game_index][1][dog_index][0]== "dog1_img":
        image (dog1_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
        
    elif data[game_index][1][dog_index][0]== "dog2_f_img":
        image (dog2_f_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
    elif data[game_index][1][dog_index][0]== "dog2_img":
        image (dog2_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
        
    elif data[game_index][1][dog_index][0]== "dog3_f_img":
        image (dog3_f_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
    elif data[game_index][1][dog_index][0]== "dog3_img":
        image (dog3_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
        
    elif data[game_index][1][dog_index][0]== "dog4_f_img":
        image (dog4_f_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)
    elif data[game_index][1][dog_index][0]== "dog4_img":
        image (dog4_img, data[game_index][1][dog_index][1]*50,data[game_index][1][dog_index][2]*50)


def dog_move(dog_number,x_move,y_move, game_index):
    global data
    data[game_index][1][dog_number][1] += x_move  
    data[game_index][1][dog_number][2] += y_move

def draw_grid(current_dog):
    strokeWeight(2)
    stroke(113,142,102)
    for x in range (11):
        line(x*50,0,x*50,500)
    for y in range (10):
        line(0,y*50,500,y*50)
    stroke(0)
    noFill()
    rect(0,0,500,499)
    
    image (menu_bg_img, 500,0)
    rect(500,0,199,499)
    rect (530, 140,150,20)
    rect (530, 220,150,20)
    fill(0)
    textSize(15)
    text("press f to \nincrease speed\npress s to \n decrease speed", 600,450)
    textSize(30)
    text("score", 600,50)
    text("dog", 600,300)
    text(current_dog, 600,350)
    text(data[current_dog][4][0], 600,80)
    text("hunger", 600, 120)
    text("thirst", 600,190)
    strokeWeight(1)
    fill (255,0,0)
    for x in range (int(data[current_dog][0][1]*2)):
        rect(530+(x*5), 140,5,20 )
    for x in range (int(data[current_dog][0][3]*2)):
        rect(530+(x*5), 220,5,20 )

    

def setup():
    size (700,500)
    frameRate(frame_rate)
    background(113,142,102)
    my_font = createFont("Silkscreen",30)
    textFont(my_font)
    textAlign(CENTER,CENTER)
    global steak_img, dog1_img, dog2_img, dog3_img, dog4_img, water_img, dog1_f_img,dog2_f_img ,dog3_f_img,dog4_f_img, pointer_img, menu_bg_img, mode
    steak_img = loadImage("steak.png")
    water_img = loadImage("water.png")
    dog1_img = loadImage("dog1.png")
    dog2_img = loadImage("dog2.png")
    dog3_img = loadImage("dog3.png")
    dog4_img = loadImage("dog4.png")
    dog1_f_img = loadImage("dog1_f.png")
    dog2_f_img = loadImage("dog2_f.png")
    dog3_f_img = loadImage("dog3_f.png")
    dog4_f_img = loadImage("dog4_f.png")
    pointer_img = loadImage("pointer.png")
    menu_bg_img = loadImage("menubg.png")

    create_data()

    mode = "running"



    


def draw():
    global time,mode, current_dog

    dead_dogs=0
    for game_index in range (number_of_games):
        if data[game_index][6][0] == 0 and mode == "running":
            dead_dogs+=1
            
    if dead_dogs == number_of_games and mode == "running":
        #natural_selection(number_of_games)
        mode = "gen setup"
        print "all dogs have died"
        gen_ended()
        
    if data[current_dog][6][0] == 0 and mode == "running":
        dog = "searching"
        search = 0
        while dog == "searching":
            search+=1

            if search == number_of_games:
                dog = "found"
                
            elif data[search][6][0] == 1:
                dog = "found"
                current_dog = search
        
  
    else:
        time += 1
        for game_index in range (number_of_games):
            if mode == "running" and data[game_index][6][0] != 0:
         
                background(156,198,138)
                draw_grid(current_dog)
                check_items(game_index)
        
                for i in range (len(data[current_dog][1])):
                    dog_show(i, current_dog)
    
                
                for i in range (len(data[current_dog][2])):
                    draw_food(0,i, current_dog)
                    
                for i in range (len(data[current_dog][3])):
                    draw_food(1,i,current_dog)
                    
                dog_show(0, current_dog)
                
                get_distances(game_index)
                choose_target(game_index)
                check_items(game_index)
                
                data[game_index][4][0] += 1
                data[game_index][0][1] += 1*starve_rate
                data[game_index][0][3] += 1*starve_rate
                seek_target(data[game_index][5][0],data[game_index][5][1],game_index) 
                
                
                            
                if data[game_index][0][1] == 15:
                    data[game_index][6][0] = 0
                    data[game_index][7][0] = "hunger"
                elif data[game_index][0][3] == 15 :
                    data[game_index][6][0] = 0
                    data[game_index][7][0] = "thirst"
    
    

    
def keyPressed():
    global frame_rate
    if key == "x":
        if mode == "setup done" :
            create_data()
    if key == "f" and mode == "running":
        frame_rate +=1
        frameRate(frame_rate)
    if key == "s" and mode == "running":
        frame_rate -=1
        frameRate(frame_rate)

    
        
    
    
