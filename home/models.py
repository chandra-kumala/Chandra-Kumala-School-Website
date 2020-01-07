from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.core.blocks import TextBlock, StructBlock
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from tools.models import Seo, CommonStreamBlock, Item


class HomePage(Page, Seo):
    heading = models.CharField(max_length=250, null=True, blank=True)
    text = RichTextField(null=True, blank=True)
    buttonLabel = models.CharField(max_length=255, null=True, blank=True)
    buttonUrl = models.URLField(null=True, blank=True)
    body = StreamField(CommonStreamBlock(required=False), null=True, blank=True)

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
        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('text'),
            FieldPanel('buttonLabel'),
            FieldPanel('buttonUrl'),
        ], "Jumbotron"),
        InlinePanel('carousel_items', label="Carousel images"),
        StreamFieldPanel('body', "Main content..."),
    ]

    promote_panels = Page.promote_panels + Seo.panels

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class Carousel(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    title = models.CharField(blank=True, max_length=250)
    caption = models.CharField(blank=True, max_length=250)
    image = models.ForeignKey('wagtailimages.Image',  null=True,
                              blank=True, on_delete=models.CASCADE, related_name='+')

    panels = [
        FieldPanel('title'),
        FieldPanel('caption'),
        ImageChooserPanel('image'),
    ]
