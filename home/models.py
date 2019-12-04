from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from tools.models import Dreamer, Seo

import datetime
dom = datetime.datetime.now().strftime ("%d")



class HomePage(Page, Dreamer, Seo):

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['menuitems'] = request.site.root_page.get_descendants(inclusive=True).live().in_menu()
        # context['menuitems'] = self.get_children().filter(live=True, show_in_menus=True)


        return context

    parent_page_types = ['wagtailcore.page', 'home.HomePage']
    subpage_types = ['tools.Index', 'tools.GoogleMaps', 'tools.GoogleCalendar', 'home.HomePage']


    content_panels = Page.content_panels + Dreamer.panels + [
        InlinePanel('carousel_items', label="Carousel images"),
    ] 
     
    promote_panels = Page.promote_panels + Seo.panels


    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class Carousel(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_items')
    title = models.CharField(blank=True, max_length=250)
    caption = models.CharField(blank=True, max_length=250)
    image = models.ForeignKey('wagtailimages.Image',  null=True, blank=True, on_delete=models.CASCADE, related_name='+')

    panels = [
        FieldPanel('title'),
        FieldPanel('caption'),
        ImageChooserPanel('image'),
    ]