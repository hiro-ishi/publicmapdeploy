#Djangoから必要な機能をインポート
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required

#GeoDjangoからインポート
from django.contrib.gis import forms
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance

#DRFからインポート
from rest_framework import viewsets, status
from rest_framework_gis.filters import DistanceToPointFilter, InBBoxFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
import traceback
import json
from django.core.serializers import serialize

#Postモデルをインポート
from .models import Post # "."indicate current directory
#Postフォームをインポート
from .forms import PostForm
#Postシリアライザーをインポート
from .serializers import PostSerializer

#ログイン前のホーム画面
def index(request):
    return render(request, 'mapping/index.html')

#メインビュー(マップ表示・一覧表示)を定義
@login_required
def map_mainview(request):
    #to create a variable for our QuerySet "Posts"
    posts = Post.objects.all().order_by('number')
    contexts = {'posts': posts}
    return render(request, 'mapping/map_mainview.html', contexts)#{'名前': クエリセット}で引数を渡す。
    #以下に地図を表示させるスクリプトが入る

#ヘルプページの定義
def map_help(request):
    return render(request, 'mapping/map_help.html')

#CRUD (Create Read Update Delete)の実装
@login_required
def post_add(request): #Formを発行したいURLに対してビューの中でインスタンス化
    if request.method == "POST": #FormのなかのPOST or GET の POST である
        form = PostForm(request.POST) #フォームにデータを”くくりつけたbounded”
        # if the form is correct (all required fields are set
        # and no incorrect values have been submitted)
        if form.is_valid():
            #commit=False means that we don't want to save the Post model yet
            post = form.save(commit=False)
            #preserve changes (adding the author) and a new blog post is created
            post.save()
            return redirect('../../map_mainview/')

    else:
        form = PostForm()
    return render(request, 'mapping/post_edit.html', {'form': form})

# we pass extra pk parameter from urls.py
@login_required
def post_edit(request, pk):
    #we get the Post model we want to edit
    post = get_object_or_404(Post, pk=pk)
    # We pass the created post as an "instance"
    if request.method == "POST": # when we save theform
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('../../../map_mainview/')
    else:
        form = PostForm(instance=post) #or, when we have just opened a form with this post to edit
    return render(request, 'mapping/post_edit.html', {'form': form})

#delete
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('../../../map_mainview/')

#API関連のビュー
#Pagination
class MyPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

# DRFの設定
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = MyPagination
    filter_backends = (DistanceToPointFilter,)
    distance_filter_field = 'geom'
    distance_filter_convert_meters = True

class GeojsonAPIView(APIView):
    def get(self, request, *args, **keywords):
        try:
            encjson  = serialize('geojson', Post.objects.all().order_by('number'),srid=4326, geometry_field='location', fields=('pk','title', 'number', 'memo') )
            result   = json.loads(encjson)
            response = Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
        except:
            response = Response({}, status=status.HTTP_404_NOT_FOUND)

        return response
