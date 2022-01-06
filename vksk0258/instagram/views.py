from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, \
    DeleteView
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm


# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # 현재 로그인 User Instance
#             post.save()
#             messages.success(request, '포스팅을 저장했습니다.')
#             return redirect(post)
#     else:
#         form = PostForm()

#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': None,
#     })


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)
    
post_new = PostCreateView.as_view()


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
    
#     # 작성자 Check Tip
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         return redirect(post)
    
#     if request.method =='POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
        
#     return render(request, 'instagram/post_form.html',{
#         'form': form,
#     })

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, '포스팅을 수정했습니다.')
        return super().form_valid(form)


post_edit = PostUpdateView.as_view()
    
# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제했습니다.')
#         return redirect('instagram:post_list')
#     return render(request, 'instagram/post_confirm_delete.html', {
#         'post' : post,
#     })

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('instagram:post_list')

    # def get_success_url(self):
    #     return reverse('instagram:post_list')


post_delete = PostDeleteView.as_view()
    
    
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
    