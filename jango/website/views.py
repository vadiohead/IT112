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

    if request.method == 'POST':
        name = request.POST.get('user', 'Mysterious guest')
        color = request.POST.get('color')
        number = request.POST.get('number')
        fortune_msg = fortunes.get((color, number), "0xc0ffee: undefined")
        return render(request, 'fortune_result.html', {
            'name': name,
            'fortune_msg': fortune_msg
        })

    return render(request, 'fortune.html')

# databases

def show_songs(request):
    songs = SongList.objects.all()
    return render(request, 'song_list.html', {'songs': songs})

def song_details(request, song_id):
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

def clear_songs(request):
    SongList.objects.all().delete()
    return render(request, 'clearance.html')

def api_handler(request):
    songs = SongList.objects.all()
    data = [{
        'id': s.id, 'title': s.title, 'album': s.album,
        'year': s.year, 'video': s.video
    } for s in songs]
    return JsonResponse(data, safe=False)


def api_song_details(request, song_id):
    try:
        song = SongList.objects.get(id=song_id)
        data = {
            'id': song.id,
            'title': song.title,
            'album': song.album,
            'year': song.year,
            'video': song.video
        }
        return JsonResponse(data, status=200)
    except SongList.DoesNotExist:
        return JsonResponse({'error': 'Song not found'}, status=404)