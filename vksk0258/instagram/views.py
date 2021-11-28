from django.shortcuts import render
from .models import Post

def post_list(request):
    qs = Post.objects.all()
    q = request.GET.get('q', '') #q가 없을 경우 ''을 반환한다
    if q:
        qs = qs.filter(message__icontains=q)
    # instagram/tamplates/instagram/post_list.html의 경로에 만든다
    return render(request, 'instagram/post_list.html',{
        'post_list': qs,
        'q': q,
    })
    