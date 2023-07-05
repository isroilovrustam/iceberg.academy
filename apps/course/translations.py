from .models import Course, Lesson, Task, ForExample
from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline


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


class TranslationsInlineAdmin(TranslationStackedInline):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@register(Course)
class Trans(TranslationOptions):
    fields = ['title', 'body']


@register(Lesson)
class Trans(TranslationOptions):
    fields = ['title']


@register(Task)
class Trans(TranslationOptions):
    fields = ['title', 'body']


@register(ForExample)
class Trans(TranslationOptions):
    fields = ['input', 'output']
