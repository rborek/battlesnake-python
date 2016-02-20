import bottle
import os

id = "c6c28e7d-0f7e-473c-a2bc-8ee6dfc4a1a2";

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


@bottle.post('/move')
def move():
    data = bottle.request.json
    grid = [[0 for i in xrange(data['width'])] for i in xrange(data['height'])]

    for snake in data['snakes']:
        # if it is us
        if snake['id'] == id:
            for coord in snake['coords']:
                print coord[0] + " " + coord[1]
                sys.stdout.flush()


    # TODO: Do things with data


    return {
        'move': 'north',
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
