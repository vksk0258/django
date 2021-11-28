from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, Tag

# 모델 클래스를 admin에 등록하는 첫번째 방법
# admin.site.register(Post)


# 모델 클래스를 admin에 등록하는 두번째 방법
# class PostAdmin(admin.ModelAdmin): #임의의 이름 PostAdmin사용
#     pass

# admin.site.register(Post, PostAdmin)


# 모델 클래스를 admin에 등록하는 세번째 방법
@admin.register(Post) #wrapping
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','photo_tag','message','message_length','is_publish','created_at','updated_at']
    list_display_links = ['message'] #자신이 원하는 항목에 링크를 걸 수 있다.
    search_fields = ['message'] # message에 관한 search바를 생성한다.
    list_filter = ['is_publish','created_at']
    
    def photo_tag(self, post):
        if post.photo: # 만약 저장된 이미지가 있다면
            return mark_safe(f'<img src="{post.photo.url}" style="width: 72px;" />') # 해당 url을 얻을 수 있다 mark_safe를 쓰면 바로 이미지를 띄울 수 있다
        return None # 없다면 반환하지 않는다 

    def message_length(self, post):
        return f"{len(post.message)} 글자"
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass