from flask import Flask, request

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

# Fortune route
@app.route('/fortune', methods=['POST', 'GET'])
def fortune():
    color = ['chartreuse', 'turquoise', 'elephant\'s breath', 'red']
    number = ['1', '2']

    if request.method == 'POST':
        name = request.form.get('user', 'Mysterious guest')
        color = request.form.get('color')
        number = request.form.get('number')

        fortunes = {
            ('chartreuse', '1'): "you are lucky",
            ('chartreuse', '2'): "peace upon you",
            ('turquoise', '1'): "fill you with wit",
            ('turquoise', '2'): "do not pick elephant\'s breath",
            ('elephant\'s breath', '1'): "phoque yew",
            ('elephant\'s breath', '2'): "straight outta compton",
            ('red', '1'): "you will find something surprising",
            ('red', '2'): "you will do something amazing"
        }
        fortune_msg = fortunes.get((color, number), "0xc0ffee: undefined")

        return f"""
            <p>{name}, your fortune is:<strong> {fortune_msg}</strong></p>
            <a href="/fortune">Try Again</a>
        """

    else:
    # GET method: display form
        return """
            <h2>Get Your Fortune</h2>
            <form method="POST" action="/fortune">
                <label>Your name: </label><br>
                <input type="text" name="user"><br><br>
    
                <label>Choose a color:</label><br>
                <select name="color">
                    <option>chartreuse</option>
                    <option>turquoise</option>
                    <option>elephant's breath</option>
                    <option>red</option>
                </select><br><br>
    
                <label>Choose a number:</label><br>
                <select name="number">
                    <option>1</option>
                    <option>2</option>
                </select><br><br>
    
                <button type="submit">Submit</button>
            </form>
        """
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')