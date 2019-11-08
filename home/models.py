from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock 
from wagtail.images.edit_handlers import ImageChooserPanel

from section.models import Streamer, Seo


class GeneralPage(Page, Streamer, Seo):
    parent_page_types = ['home.HomePage']
    subpage_types = ['items.Index']


    content_panels = Page.content_panels + Streamer.panels
     
    promote_panels = Page.promote_panels + Seo.panels


    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

class HomePage(Page):
    intro = RichTextField(blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('carousel_items', label="Carousel images"),
        StreamFieldPanel('body', classname="full"),
    ]


class HomePageRelatedLink(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_items')
    title = models.CharField(blank=True, max_length=250)
    caption = models.CharField(blank=True, max_length=250)
    image = models.ForeignKey('wagtailimages.Image',  null=True, blank=True, on_delete=models.CASCADE, related_name='+')


    panels = [
        FieldPanel('title'),
        FieldPanel('caption'),
        ImageChooserPanel('image'),

    ]
