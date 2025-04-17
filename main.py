from flask import Flask

app = Flask(__name__)

# Default route
@app.route('/')
def home():
    return "<h1>Flash</h1>"

# About route
@app.route('/about')
def about():
    return """
        <h2>About Me</h2>
        <p>Wah gwaan people, I'm Clyde.</p>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')