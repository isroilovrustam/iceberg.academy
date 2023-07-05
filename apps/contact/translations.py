from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TranslationAdmin

from .models import About, Goal


class CustomTranslationsAdmin(TranslationAdmin):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
@register(About)
class Trans(TranslationOptions):
    fields = ['title', 'body']
@register(Goal)
class Trans(TranslationOptions):
    fields = ['title', 'body']