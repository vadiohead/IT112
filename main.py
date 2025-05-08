from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'

db = SQLAlchemy(app)

@app.route('/')
def home():
    return """
        <h1>Flash</h1>
        <a href='/about'>About Me</a>
        <br>
        <a href='/fortune'>Get Your Fortune</a>
        <br>
        <a href='/songs'>Songs</a>
        <br>
    """

@app.route('/about')
def about():
    return """
        <h2>About Me</h2>
        <p>Wah gwaan people, I'm Clyde.</p>
        <a href="/">Main Page</a>
    """

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
                <br>
                <a href="/">Main Page</a>
            </form>
        """

# databases

class SongList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    album = db.Column(db.String())
    year = db.Column(db.Integer)
    video = db.Column(db.String())

    def __init__(self, title, album, year, video):
        self.title = title
        self.album = album
        self.year = year
        self.video = video

#def populate_db():
    #db.create_all()
    #songs = [
    #        SongList(title='Ice Cube - My Summer Vacation', album='Death Certificate', year=1991,
    #                 video='https://youtube.com/watch?v=SXrWIyCW-7E'),
    #        SongList(title='Car Seat Headrest - Gethsemane', album='The Scholars', year=2025,
    #                 video='https://youtu.be/RAGA2fmBSJo?si=FtCJZZyGhYmnvUcn'),
    #        SongList(title='The Beloved - Sweet Harmony', album='Conscience', year=1993,
    #                 video='https://youtu.be/rP9Z5Pc8cRM?si=1nSsg7XkPkwBNPIo'),
    #       SongList(title='Yeule - sulky baby', album='softscars', year=2023,
    #                 video='https://youtu.be/ca7zUSNpL70?si=Yo9sk9hmVYip0pCD'),
    #        SongList(title='Noize MC - Ругань из-за стены', album='Последний альбом', year=2010,
    #                 video='https://youtu.be/vr1qkx3hfx8?si=kGrhs0Dy_mMRPykZ'),
    #        SongList(title='Alihan Dze - Бухы дээрэ (ft. Saryuna)', album='Шата', year=2016,
    #                 video='https://youtu.be/vP3oc-pHRtE?si=AmdcESSAb4hU2ojZ')
    #]
    #db.session.bulk_save_objects(songs)
    #db.session.commit()

@app.route('/songs')
def show_songs():
    songs = SongList.query.all()
    song_list = "".join([f"<li><a href='/songs/{song.id}'>{song.title}</a></li>" for song in songs])
    return f"""
        <h2>Song list</h2>
        <ul>{song_list}</ul>
        <a href="/songs/add">Add a New Song</a><br><br>
        <a href="/">Main Page</a>
    """

@app.route('/songs/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form.get('title')
        album = request.form.get('album')
        year = request.form.get('year')
        video = request.form.get('video')
        
        if not title or not album or not year or not video:
            return """
                <p>All fields are required!</p>
                <a href="/songs/add">Go Back</a>
            """

        try:
            year = int(year)
        except ValueError:
            return """
                <p>Year must be a valid number!</p>
                <a href="/songs/add">Go Back</a>
            """

        new_song = SongList(title=title, album=album, year=year, video=video)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('show_songs'))

    return """
        <h2>Add a New Song</h2>
        <form method="POST">
            Title:           <input type="text" name="title"><br><br>
            Album:           <input type="text" name="album"><br><br>
            Year:            <input type="text" name="year"><br><br>
            Music Video URL: <input type="text" name="video"><br><br>
            <input type="submit" value="Add Song">
        </form>
        <br>
        <a href="/songs">Back to Songs List</a>
    """

@app.route('/songs/<int:song_id>')
def song_detail(song_id):
    song = SongList.query.get_or_404(song_id)
    return f"""
        <h2>{song.title}</h2>
        <p><strong>Album:</strong> {song.album}</p>
        <p><strong>Year of release:</strong> {song.year}</p>
        <p><strong>Music video: </strong>
            <a href="{song.video}" target="_blank">{song.video}</a>
        </p>
        <a href="/songs">Back to Songs List</a>
    """

@app.route('/clear-db')
def clear_songs():
    SongList.query.delete()
    db.session.commit()
    return "<p>Database has been cleared.</p><a href='/'>Go to Main Menu</a>"

if __name__ == '__main__':
    #with app.app_context():
    #    populate_db()
    app.run(debug=True, host='0.0.0.0')