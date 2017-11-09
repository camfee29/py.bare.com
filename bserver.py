from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/get/<name>/<id>')
def index(name, id):
    return template('<b>get {{name}} {{id}}</b>!', name=name, id=id)

run(host='localhost', port=8080)
