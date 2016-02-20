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
            for coord in snake['coords']:
                grid[coord[0]][coord[1]] = 1
    return grid

def getSafeMovesBasedOnOtherSnakes(data):
    grid = getGridOfPossibleMovesByOtherSnakes(data)
    me = getMe(data)
    head = me['coords'][0]
    safeMoves = []
    return safeMoves

@bottle.post('/move')
def move():
    data = bottle.request.json
    grid = getGrid(data) 
    toMove = 'north'
    head = [0, 0]
    for snake in data['snakes']:
        # if it is us
        if snake['id'] == id:
            head = snake['coords'][0]
            justMovedX = snake['coords'][0][0]-snake['coords'][1][0]
            justMovedY = snake['coords'][0][1]-snake['coords'][1][1]
            if justMovedX ==0:
                if(justMovedY>0):
                    justMoved = "Moved south"
                else:
                    justMoved = "Moved north"
            else: 
                if(justMovedX>0):
                    justMoved ="Moved east"
                else:
                    justMoved = "Moved west"
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
