from django.db import models
from django.conf import settings
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%m/%d') # pip install pillow 설치 이미지처리 할때 사용 이미지같은 경우 경로만 db에 저장되고 이미지는 파일스토리지에 저장된다
                                                                               # upload to는 파일을 정리해서 저장할 때 사용
    is_publish = models.BooleanField(default=False, verbose_name='공개여부')
    tag_set = models.ManyToManyField('Tag', blank=True) # Tag를 문자열로 넣는 이유는 Tag라는 클래스를 참조하려고 하지만 위에 아직 나오지 않아서 Tag를 바로 참조할 수 없다 그래서 문자열로 지정해놓는다
                                                        # blank=True를 해놓는 이유는 게시물에 태그를 안 달수도 있다. 그렇지 않으면 장고 폼에서 유효성 검사를 할때 태그를 안달았다고 에러가 뜬다
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        #return f"Custom Post object ({self.id})" #목록의 이름을 변환
        return self.message #목록의 이름을 메시지로 변환
    
    def get_absolute_url(self):
        return reverse("instagram:post_detail", args={self.pk})
    
    class Meta:
        ordering = ['-id']
    
    # def message_length(self):
    #     return len(self.message)
    # message_length.short_description = "message 글자 수" #항목의 이름을 변경 할 수도 있다.
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, # Post모델과 관계가 있다. CASCADE는 1측의 모델이 삭제될때 관련된 데이터들은 다 같이 삭제한다.
                             limit_choices_to={'is_publish': True}) # post에서 is_public이 True일때만 사용하겠다.
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    #post_set = models.ManyToManyField(Post)
    
    def __str__(self):
        return self.name