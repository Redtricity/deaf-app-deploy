from django import forms
from .models import Video
from .models import Post
from .models import Community
from .models import Comment

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'caption', 'location', 'description']
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'video', 'community']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['community'].queryset = user.joined_communities.all()
            self.fields['community'].label = "Post to Community"
            

    
class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'is_public', 'image']  
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


def mycommunity(request):
    communities = Community.objects.all()  
    return render(request, 'mycommunity.html', {'communities': communities})

def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            community.members.add(request.user)  
            return redirect('mycommunity')
    else:
        form = CommunityForm()
    return render(request, 'create_community.html', {'form': form})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add a comment...'
            })
        }