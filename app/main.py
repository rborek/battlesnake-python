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

def getEmptyGrid():
    return [[0 for row in range(data['width'])] for col in range(data['height'])];

def getMe(data):
    for snake in data['snakes']:
        if snake['id'] == id:
            return snake

def getGrid(data):
    grid = getEmptyGrid()
    for snake in data['snakes']:
        for coord in snake['coords']:
            grid[coord[0]][coord[1]] = 1
    return grid

def getGridOfPossibleMovesByOtherSnakes(data):
    grid = getEmptyGrid()
    for snake in data['snakes']
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
            if head[0] == 0 :
                toMove = 'north'
            elif head[0] == data['width'] - 1:
                toMove = 'south'
            if head[1] == 0:
                toMove = 'east'
            elif head[1] == data['height'] - 1:
                toMove = 'west'

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
