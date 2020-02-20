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
from wagtail.snippets.models import register_snippet
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

class Seo(models.Model):
    ''' Add extra seo fields to pages such as icons. '''
    google_ad_code = models.CharField(max_length=50, null=True, blank=True)
    seo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional social media image 300x300px image < 300kb."
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('seo_image'),
                FieldPanel('google_ad_code'),
            ],
            heading="Additional SEO options ...",
        )

    ]

    class Meta:
        """Abstract Model."""

        abstract = True

@register_snippet
class Google(models.Model):
    site_tag = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Google site code"
        verbose_name_plural = "Google site code"

    panels = [
        FieldPanel('site_tag'),
    ]

    def __str__(self):
        return self.site_tag

@register_snippet
class Facebook(models.Model):
    site_tag = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Facebook site code"
        verbose_name_plural = "Facebook site code"

    panels = [
        FieldPanel('site_tag'),
    ]

    def __str__(self):
        return self.site_tag

@register_snippet
class Social(models.Model):
    css = models.CharField("List CSS Classes (eg. text-primary py-0)",
                           max_length=255, null=True, blank=True)  # eg. text-primary py-0 fa-2x
    title = models.CharField("Desc on hover (eg. December Bulletin)", max_length=255,
                             null=True, blank=True)  # eg. Latest School Bulletin
    link = models.CharField(
        "Link to resource (eg tel:+62-061-661-6765)", max_length=255, null=True, blank=True)
    icon = models.CharField(
        "FA Icon (eg. fas fa-newspaper fa-fw fa-2x)", max_length=255, null=True, blank=True)
    text = models.CharField("Visible text (eg. Latest School Bulletin)",
                            max_length=255, null=True, blank=True)  # eg. Decembers Bulletin

    class Meta:
        verbose_name = "Social Media link and icon"
        verbose_name_plural = "Social Media links and icons"


    panels = [
        FieldPanel('css'),
        FieldPanel('link'),
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

class HomePage(Page, Seo):
    my_stream = StreamField(CommonStreamBlock(required=False), null=True, blank=True)

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['menuitems'] = request.site.root_page.get_descendants(
            inclusive=True).live().in_menu()

        return context

    parent_page_types = ['wagtailcore.page', 'home.HomePage']
    subpage_types = ['home.HomePage','tools.Index', 'contact.ContactPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('my_stream', "Main content..."),
    ]

    promote_panels = Page.promote_panels + Seo.panels

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

