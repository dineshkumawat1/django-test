from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .models import BlogCategory, BlogPost, BlogReaction, Comment, CommentReaction
from apps.blogs.forms import BlogCategoryForm ,BlogPostForm
from .models import BlogCategory, BlogPost, BlogReaction, Comment, CommentReaction

def get_image_preview(obj):
    if obj.pk and obj.thumbnail :
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.thumbnail)
                         # return mark_safe("""<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" /></a>""".format(
                         #     src=obj.picture.url,
                         #     title=obj.product_id,
                         # )
                         )

    return _("(choose a picture and save and continue editing to see the preview)")

get_image_preview.short_description = _("Picture Preview")


admin.site.index_title = 'Django Test Admin'
admin.site.site_header = 'Analytics Steps'
admin.site.index_title = 'Test Site Administrator'


class BlogCategoryAdmin(admin.ModelAdmin):
    form = BlogCategoryForm
    list_display = ('name', 'is_active', 'status')
    list_filter = ('is_active', 'status', 'parent')
    prepopulated_fields = {"slug": ("name",)}

    fields = ['name', 'slug', 'parent', 'description',  'meta_title', 'meta_description',
              'meta_keywords',
              'head_script', 'is_active', 'status', 'created_on', 'updated_on','thumbnail','select_thumbnail',get_image_preview]
    readonly_fields = ['thumbnail',get_image_preview]

admin.site.register(BlogCategory, BlogCategoryAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ('title', 'created_by', 'is_active', 'status', 'updated_by')
    list_filter = ('is_active', 'status', 'category', 'is_published', 'is_featured')
    prepopulated_fields = {"slug": ("title",)}
    fields = ['category', 'title', 'slug', 'excerpt',  'contents', 'tags',
              'is_published','head_script','is_active','status','created_on','created_by','updated_on','updated_by',
              'published_on', 'is_featured', 'meta_title', 'meta_description', 'meta_keywords','view_count',
              'thumbnail','select_thumbnail',get_image_preview]
    readonly_fields = ['thumbnail', get_image_preview]


admin.site.register(BlogPost, BlogPostAdmin)


class BlogReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_on')
    list_filter = ('blog',)


admin.site.register(BlogReaction, BlogReactionAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'comment', 'is_approved')
    list_filter = ('blog',)


admin.site.register(Comment, CommentAdmin)


class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_on')
    list_filter = ('comment',)


admin.site.register(CommentReaction, CommentReactionAdmin)



def show_document(obj):
    if obj.pk:
        return mark_safe('<a href="%s">%s</a>' % (obj.document, obj.document))
    return _("(No Document are entered)")
show_document.allow_tags = True
show_document.short_description = _("document")



class BlogRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_published', 'created_on')
    list_filter = ('user',)
    fields = ['user',show_document,'is_published','updated_on']
    readonly_fields = [show_document]

