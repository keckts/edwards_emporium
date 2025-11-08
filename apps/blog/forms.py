from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, HTML, Layout, Row
from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "content",
            "status",
            "topic",
            "image",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"id": "quill-content", "class": "d-none"}),
            "slug": forms.TextInput(
                attrs={
                    "placeholder": "Leave blank to auto-generate from title",
                    "class": "input input-bordered w-full",
                }
            ),
        }
        help_texts = {
            "slug": "URL-friendly version of the title. Leave blank to auto-generate.",
            "content": "Use the editor below to create your blog post content.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            "title",
            "slug",
            Row(
                Column("status", css_class="form-group col-md-4 mb-0"),
                Column("topic", css_class="form-group col-md-4 mb-0"),
                Column("image", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Div(
                HTML(
                    """
                    <div class="form-group mb-4">
                        <label class="form-label">Content</label>
                        <div id="quill-editor" style="height: 400px; background: white;"></div>
                        <small class="form-text text-muted">{{ form.content.help_text }}</small>
                    </div>
                    """
                ),
                css_class="mb-4",
            ),
            "content",
        )
