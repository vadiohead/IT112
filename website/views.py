from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import SongList

def home(request):
    user_name = request.GET.get('user_name', '')
    return render(request, 'base.html', {'user_name': user_name})

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
    return render(request, 'song_list.html', {'songs': songs})

def song_detail(request, song_id):
    song = get_object_or_404(SongList, id=song_id)
    return render(request, 'song_details.html', {'song': song})

def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        album = request.POST.get('album')
        year = request.POST.get('year')
        video = request.POST.get('video')

        if not title or not album or not year or not video:
            return render(request, 'add_song.html', {
                'error': 'All fields are required.'
            })

        try:
            year = int(year)
        except ValueError:
            return render(request, 'add_song.html', {
                'error': 'Year must be a valid number.'
            })

        SongList.objects.create(title=title, album=album, year=year, video=video)
        return redirect('/songs')

    return render(request, 'add_song.html')

def api_handler(request):
    songs = SongList.objects.all()
    data = [{
        'id': s.id, 'title': s.title, 'album': s.album,
        'year': s.year, 'video': s.video
    } for s in songs]
    return JsonResponse(data, safe=False)

def clear_songs(request):
    SongList.objects.all().delete()
    return render(request, 'clearance.html')