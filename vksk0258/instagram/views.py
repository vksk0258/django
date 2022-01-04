from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView,DetailView,ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm

def post_new(request):
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostForm()
        
    return render(request, 'instagram/post_form.html',{
        'form': form,
    })

# CBV방식으로 post_list 구현하기
# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))

# @method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10

post_list = PostListView.as_view()
     

# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '') #q가 없을 경우 ''을 반환한다
#     if q:
#         qs = qs.filter(message__icontains=q)
#     # instagram/tamplates/instagram/post_list.html의 경로에 만든다
#     return render(request, 'instagram/post_list.html',{
#         'post_list': qs,
#         'q': q,
#     })
    
# 어떠한 정수가 넘어올때
# def post_detail(request : HttpRequest, pk : int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     # try:
#     #     post = Post.objects.get(pk=pk) # DoseNotExist 예외처리 데이터 응답을 보냈는데 데이터가 없을때
#     # except Post.DoesNotExist:
#     #     raise Http404
#     return render(request, 'instagram/post_detail.html', {
#         'post' : post,
#     })

# post_detail = DetailView.as_view(model = Post, queryset=Post.objects.filter(is_publish=True)) # 쿼리셋 필터를 넣을 수도 있다.

class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_publish=True)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated: # 로그인 인증
            qs = qs.filter(is_publish=True) # 로그인이 되어있지 않다면 공개된부분들만 봐라
        qs = qs.filter()
        return qs
    
post_detail = PostDetailView.as_view()
    

# def archives_year(request, year):
#     return HttpResponse(f"{year}년")

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at')
    