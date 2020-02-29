from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.gis import forms # as geoforms
from django.contrib.gis.forms import OSMWidget, PointField, ModelForm
from .models import CustomUser, Post

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class PostForm(forms.ModelForm):
#モデルで定義された条件をオーバーライドする（Metaの記述より先に書く）
    memo = forms.CharField(widget = forms.Textarea)
    location = forms.PointField(
            widget = OSMWidget(
                attrs = {'map_width': 570, 'map_height': 570,
                        'template_name':'gis/openlayers-osm.html',
                        'default_lon' : 141.34964,
                        'default_lat' : 43.06417,
                        'default_zoom' : 8}))
    class Meta:
        model = Post
        fields = ('title','number','memo', 'location')

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.20.1/ol.css',
                'gis/css/ol3.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.20.1/ol.js',
            'gis/js/OLMapWidget.js',
        )
