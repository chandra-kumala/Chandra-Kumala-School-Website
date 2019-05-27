from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]


class HomePageRelatedLink(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='related_links')
    image = models.ForeignKey('wagtailimages.Image',  null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
