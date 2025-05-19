from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Shops)
class ShopsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'info')


@register(Products)
class ProductsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'title')