from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment, Tag

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill tags_text for edits
        if self.instance and self.instance.pk:
            current = ", ".join(self.instance.tags.values_list("name", flat=True))
            self.fields["tags_text"].initial = current

    def save(self, commit=True):
        post = super().save(commit=commit)
        # Parse tags after saving the post (need pk for M2M)
        tags_text = self.cleaned_data.get("tags_text", "")
        names = [t.strip() for t in tags_text.split(",") if t.strip()]
        tag_objs = []
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)
        if commit:
            post.tags.set(tag_objs)  # replace set
        else:
            # If not committed yet, defer setting M2M to caller
            self._pending_tags = tag_objs
        return post

class ProfileForm(forms.ModelForm):
    tags_text = forms.CharField(
    required=False,
    help_text="Comma-separated tags (e.g. python, django, web).",
    label="Tags",
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment…"}),
        }
