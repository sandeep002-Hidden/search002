from flask import Flask

appe = Flask(__name__)
appe.run(debug=True)

@appe.route('/')
def hello_world():
    return 'Hello, World!'
@appe.route('/hello')
def hello_wrld():
    return '<h1>Hello</h1>'

