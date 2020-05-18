from blog.forms import PostForm
from blog.models import Post


class SimplePostForm(PostForm):
    class Meta(PostForm.Meta):
        model = Post
        fields = ["author", "title", "body", "bibliography"]


class FullPostForm(PostForm):
    class Meta(PostForm.Meta):
        model = Post
        fields = "__all__"
