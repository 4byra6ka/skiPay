from django import forms

from posts.models import Posts


class AddPostMyForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'is_published', 'paid_published', 'cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})
        self.fields["paid_published"].widget.attrs.update({"class": "form-check-input"})
        self.fields["cost"].widget.attrs.update({"class": "form-control"})


class UpdatePostMyForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'is_published', 'paid_published', 'cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
        self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})
        self.fields["paid_published"].widget.attrs.update({"class": "form-check-input"})
        self.fields["cost"].widget.attrs.update({"class": "form-control"})
