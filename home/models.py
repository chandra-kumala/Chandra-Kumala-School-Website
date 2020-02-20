from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.core.blocks import (
    URLBlock, 
    TextBlock, 
    StructBlock, 
    ListBlock,
    StreamBlock, 
    CharBlock, 
    RichTextBlock, 
    BooleanBlock
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from tools.models import Seo, Item


class CarouselBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock("Title ...", blank=True, max_length=250)
    caption = TextBlock(required=False, blank=True)
    button = TextBlock(required=False)
    link = URLBlock(required=False)
 
    class Meta:
        icon = 'image'


class CommonStreamBlock(StreamBlock):
    heading = CharBlock(classname="full title", blank=True)
    paragraph = RichTextBlock(blank=True)
    embed = EmbedBlock(blank=True)
    image = ImageChooserBlock(blank=True)
    mapurl = CharBlock("Google Map URL", max_length=500, null=True, blank=True)
    calendarurl = URLBlock("URL for calendar", null=True, blank=True)
    buttonLink = StructBlock([
        ('text', TextBlock(blank=True)),
        ('link', URLBlock(label="external URL", blank=True)),
    ])
    buttonLink = StructBlock([
        ('text', TextBlock(blank=True)),
        ('link', URLBlock(label="external URL", blank=True)),
    ])
    jumbotron = StructBlock([
        ('heading', CharBlock(classname="full title", blank=True)),
        ('classes', CharBlock(label="CSS classes from BS (text-light or text-dark)", required=False, blank=True)),
        ('text', TextBlock(required=False, blank=True)),
        ('buttonLabel', CharBlock(required=False, label="Text on button", blank=True)),
        ('buttonUrl', URLBlock(required=False, blank=True)),
        ('background', ImageChooserBlock(required=False, blank=True)),
    ])
    testimonial = StructBlock([
        ('test_name', TextBlock(blank=True)),
        ('test_quote', TextBlock(blank=True)),
        ('test_reversed', BooleanBlock(required=False, default=False)),
        ('test_pic', ImageChooserBlock(blank=True)),
    ])
    carousel = ListBlock(CarouselBlock(), icon="image", null=True, blank=True)


    class Meta:
        icon = 'cogs'

class HomePage(Page, Seo):
    my_stream = StreamField(CommonStreamBlock(required=False), null=True, blank=True)

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['menuitems'] = request.site.root_page.get_descendants(
            inclusive=True).live().in_menu()

        return context

    parent_page_types = ['wagtailcore.page', 'home.HomePage']
    subpage_types = ['tools.Index', 'tools.GoogleMaps',
                     'tools.GoogleCalendar', 'home.HomePage',
                     'contact.ContactPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('my_stream', "Main content..."),
    ]

    promote_panels = Page.promote_panels + Seo.panels

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

