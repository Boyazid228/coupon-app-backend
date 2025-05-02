from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name',)