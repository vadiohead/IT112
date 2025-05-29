from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import SongList

def home(request):
    return HttpResponse("""
        <h1>Django</h1>
        <a href='/about'>About Me</a><br>
        <a href='/fortune'>Get Your Fortune</a><br>
        <a href='/songs'>Songs</a><br>
    """)

def about(request):
    return HttpResponse("""
        <h2>About Me</h2>
        <p>Wah gwaan people, I'm Clyde.</p>
        <a href="/">Main Page</a>
    """)

def fortune(request):
    colors = ['chartreuse', 'turquoise', "elephant's breath", 'red']
    numbers = ['1', '2']

    if request.method == 'POST':
        name = request.POST.get('user', 'Mysterious guest')
        color = request.POST.get('color')
        number = request.POST.get('number')

        fortunes = {
            ('chartreuse', '1'): "you are lucky",
            ('chartreuse', '2'): "peace upon you",
            ('turquoise', '1'): "fill you with wit",
            ('turquoise', '2'): "do not pick elephant's breath",
            ("elephant's breath", '1'): "phoque yew",
            ("elephant's breath", '2'): "straight outta compton",
            ('red', '1'): "you will find something surprising",
            ('red', '2'): "you will do something amazing"
        }
        fortune_msg = fortunes.get((color, number), "0xc0ffee: undefined")

        return HttpResponse(f"""
            <p>{name}, your fortune is:<strong> {fortune_msg}</strong></p>
            <a href="/fortune">Try Again</a>
        """)

    else:
        return HttpResponse("""
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
        """)

def show_songs(request):
    songs = SongList.objects.all()
    song_list = "".join([f"<li><a href='/songs/{song.id}'>{song.title}</a></li>" for song in songs])
    return HttpResponse(f"""
        <h2>Song list</h2>
        <ul>{song_list}</ul>
        <a href="/songs/json">Get songs in JSON file</a><br><br>
        <a href="/songs/add">Add a New Song</a><br><br>
        <a href="/">Main Page</a>
    """)

def api_handler(request):
    if request.method == 'GET':
        songs = SongList.objects.all()
        song_data = [
            {
                'id': song.id,
                'title': song.title,
                'album': song.album,
                'year': song.year,
                'video': song.video
            } for song in songs
        ]
        return JsonResponse(song_data, safe=False)

def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        album = request.POST.get('album')
        year = request.POST.get('year')
        video = request.POST.get('video')

        if not title or not album or not year or not video:
            return HttpResponse("""
                <p>All fields are required!</p>
                <a href="/songs/add">Go Back</a>
            """)

        try:
            year = int(year)
        except ValueError:
            return HttpResponse("""
                <p>Year must be a valid number!</p>
                <a href="/songs/add">Go Back</a>
            """)

        SongList.objects.create(title=title, album=album, year=year, video=video)
        return redirect('/songs')

    return HttpResponse("""
        <h2>Add a New Song</h2>
        <form method="POST">
            Title: <input type="text" name="title"><br><br>
            Album: <input type="text" name="album"><br><br>
            Year: <input type="text" name="year"><br><br>
            Music Video URL: <input type="text" name="video"><br><br>
            <input type="submit" value="Add Song">
        </form>
        <br>
        <a href="/songs">Back to Songs List</a>
    """)

def song_detail(request, song_id):
    song = get_object_or_404(SongList, id=song_id)
    return HttpResponse(f"""
        <h2>{song.title}</h2>
        <p><strong>Album:</strong> {song.album}</p>
        <p><strong>Year of release:</strong> {song.year}</p>
        <p><strong>Music video: </strong>
            <a href="{song.video}" target="_blank">{song.video}</a>
        </p>
        <a href="/songs">Back to Songs List</a>
    """)

def clear_songs(request):
    SongList.objects.all().delete()
    return HttpResponse("<p>Database has been cleared.</p><a href='/'>Go to Main Menu</a>")
