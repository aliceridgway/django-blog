from django.utils.text import slugify
# from .models import Post

def get_post_slug(post, max_length):
    title_slug = slugify(post.title)[0:max_length].strip('-')
    slug_count = Post.objects.filter(slug=title_slug, author=post.author).count()

    if slug_count == 0:
        return title_slug
    else:
        return f"{title_slug}-{slug_count+1}"