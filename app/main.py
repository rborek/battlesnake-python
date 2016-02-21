import bottle
import os

id = "c6c28e7d-0f7e-473c-a2bc-8ee6dfc4a1a2"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#44D55C',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }

def getEmptyGrid(data):
    return [[0 for row in range(data['width'])] for col in range(data['height'])];

def getMe(data):
    for snake in data['snakes']:
        if snake['id'] == id:
            return snake

def getGrid(data):
    grid = getEmptyGrid(data)
    for snake in data['snakes']:
        for coord in snake['coords']:
            grid[coord[0]][coord[1]] = 1
    return grid

def getGridOfPossibleMovesByOtherSnakes(data):
    grid = getEmptyGrid(data)
    for snake in data['snakes']:
        if snake['id'] != id:
            justMovedX = snake['coords'][0][0]-snake['coords'][1][0]
            justMovedY = snake['coords'][0][1]-snake['coords'][1][1]
            head = snake['coords'][0]
            if justMovedX ==0:
                if(justMovedY>0):
                    justMoved = "south"
                else:
                    justMoved = "north"
            else: 
                if(justMovedX>0):
                    justMoved ="east"
                else:
                    justMoved = "west"
            if justMoved != "south":
                if head[1] < 16:
                    grid[head[0]][head[1] + 1] = 1 
            if justMoved != "north":
                if head[1] > 0:
                    grid[head[0]][head[1] - 1] = 1 
            if justMoved != "east":
                if head[0] > 0: 
                    grid[head[0] - 1][head[1]] = 1 
            if justMoved != "west":
                if head[0] < 16:
                    grid[head[0] + 1][head[1]] = 1 
    return grid

def getSafeMovesBasedOnOtherSnakes(data):
    grid = getGridOfPossibleMovesByOtherSnakes(data)
    me = getMe(data)
    head = me['coords'][0]
    safeMoves = []
    if (head[0] < 16):
        if grid[head[0] + 1][head[1]] == 0:
            safeMoves.append("east")
    if (head[0] > 0):
        if grid[head[0] - 1][head[1]] == 0:
            safeMoves.append("west")
    if (head[1] < 16):
        if grid[head[0]][head[1] + 1] == 0:
            safeMoves.append("south")
    if (head[1] > 0):
        if grid[head[0]][head[1] - 1] == 0:
            safeMoves.append("north")
    return safeMoves

def returnPossibleMoves(data):
    head = snake['coords'][0]
            possibleMove = [];
            justMovedX = snake['coords'][0][0]-snake['coords'][1][0]
            justMovedY = snake['coords'][0][1]-snake['coords'][1][1]
            if justMovedX ==0:
                if(justMovedY>0):
                    justMoved = "Moved south"
                    possibleMove.append([snake['coords'][0][0]+1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0]-1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]+1])
                else:
                    justMoved = "Moved north"
                    possibleMove.append([snake['coords'][0][0]+1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0]-1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]-1])
            else: 
                if(justMovedX>0):
                    justMoved ="Moved east"
                    possibleMove.append([snake['coords'][0][0]+1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]+1])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]-1])
                else:
                    justMoved = "Moved west"
                    possibleMove.append([snake['coords'][0][0]-1,snake['coords'][0][1]])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]+1])
                    possibleMove.append([snake['coords'][0][0],snake['coords'][0][1]-1])
            moves = []
            for move in possibleMove:
                if grid[move[0]][move[1]] ==0:
                    moves.append(move)
            listToMove = []
            #turn willMove into the actual direction that the snake will move
            for willMove in move:
                if(willMove[0]-head[0]==0):
                    if(willMove[1]-head[1]==1):
                        listToMove.append("south")
                    else:
                        listToMove.append("north")
                elif willMove[0]-head[0]==1:
                    listToMove.append("east")
                elif willMove[0]-head[0]==-1:
                    listToMove.append("west")
    return listToMove

@bottle.post('/move')
def move():
    data = bottle.request.json
    grid = getGrid(data) 
    toMove = 'north'
    head = [0, 0]
    for snake in data['snakes']:
        # if it is us
        if snake['id'] == id:
            

            ### check if hit border-strongest argument        

            if head[1] == 0:
                toMove = "east"
            elif head[1] == data['height'] - 1:
                toMove = "west"
            
            # if the xcoord is 0, or to the left
            if head[0] == 0 :
                if head[1]== data['height']-1: #bottom left corner
                    if justMoved == "Moved south":
                        toMove = "east"
                    elif justMoved == "Moved west":
                        toMove = "north"
                elif head[1] == 0: # top left corner
                    if justMoved == "Moved north":
                        toMove = "east"
                    elif justMoved == "Moved west":
                        toMove = "south"
                else:
                    toMove= "north"
            #if the xcoord is to the right
            elif head[0] == data['width'] - 1:
                print "reached right side" 
                if head[1] == data['height']-1: #bottom right corner
                    if justMoved == "Moved east":
                        toMove = "north"
                    elif justMoved == "Moved south":
                        toMove = "west"
                elif head[1] == 0: # top right corner
                    print "reached top right"
                    print justMoved
                    if justMoved == "Moved north":
                        toMove = "west"
                    elif justMoved == "Moved east":
                        toMove = "south"
                else:
                    toMove = "south"
            #if the ycoord is on the bottom


    # TODO: Do things with data

    print "head at " + str(head[0]) + ", " + str(head[1]) + "moving " + toMove
    return {
        'move': toMove,
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
