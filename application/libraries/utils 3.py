from channels.db import database_sync_to_async
from apps.blogs.models import BlogPost

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_blog_or_error(blog_id, user):
    """
    Tries to fetch a kitchen for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        pass
    # Find the room they requested (by ID)
    try:
        blog = BlogPost.objects.get(pk=blog_id)

    except BlogPost.DoesNotExist:
        blog = ""
    return blog
