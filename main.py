from bottle import request, route, run, template

# @route('/')
# def index():
#     return '<b>Hello world</b>!'
@route('/')
def login():
    return '''
		<h2>Telegram sign in</h2>
        <form action="/" method="post">
            Sign in code: <input name="sign_in_code" type="text" />
            <input value="Submit" type="submit" />
        </form>
    '''

@route('/', method='POST')
def do_login():
    sign_in_code = request.forms.get('sign_in_code')
    if sign_in_code=='12345':
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

run(host='localhost', port=8080)
print('also running this')
