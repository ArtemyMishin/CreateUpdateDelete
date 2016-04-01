# -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):#модель категории
    name = models.CharField(max_length = 30, unique = True,verbose_name="Категория")#поле имя категории
    def __str__(self):
        return self.name #вывод поля в админку
    class Meta:#вывод группы
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Good(models.Model):#модель объекта (марка описание наличие категория)
    name = models.CharField(max_length = 50, unique = True, verbose_name="Марка")#имя марки
    description = models.TextField(verbose_name="Описание")#поле описание
    in_stock = models.BooleanField(default=True, db_index= True, verbose_name="В наличии")#поле наличие
    category = models.ForeignKey(Category, null=True, blank=True, on_delete= models.SET_NULL, verbose_name="Категории")#поле с выпадающим списком

    def __str__(self):
        s = self.name
        if not self.in_stock:
            s = s + u" (Net)"
        return s

    class Meta:#вывод группы объектов
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

