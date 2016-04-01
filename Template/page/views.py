# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from page.models import Category, Good
from django.core.paginator import Paginator, InvalidPage
#
# def index(request, cat_id):#контроллер index имеет параметры request(запрос) и номер категории от собственного урла
#     try:#обработка исключений
#         page_num = request.GET["page"]#номер страницы
#     except KeyError:#пустой словарь
#         page_num = 1#номер 1
#     cats = Category.objects.all().order_by("name")# переменная , хранящая список категорий
#     if cat_id == None:# если параметра cat_id из урла собственного приложения нет (пуст)
#         cat = Category.objects.first()#то переменная cat будет хранить 1ую категорию
#     else:
#         cat = Category.objects.get(pk=cat_id)#иначе категорию , индекс которой передан cat_id
#     paginator = Paginator(Good.objects.filter(category=cat).order_by("name"),1)#пагинатор,обрабатывающий объекты категории(фильр по именам объекта)
#     try:#обработка исключений
#         goods = paginator.page(page_num)
#     except InvalidPage:
#         goods = paginator.page(1)
#     return render(request, "index.html", {"category": cat, "cats": cats, "goods": goods})
#
# def good(request, good_id):
#     try:#обработка исключений
#         page_num = request.GET["page"]#номер страницы
#     except KeyError:#пустой словарь
#         page_num = 1#номер 1
#     cats = Category.objects.all().order_by("name")
#     try:
#         good = Good.objects.get(pk=good_id)
#     except Good.DoesNotExist:
#         raise Http404
#     return render(request,"good.html", {"good": good,"cats": cats,"pn": page_num})