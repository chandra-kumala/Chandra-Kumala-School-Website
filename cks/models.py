from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

class Dreamer(models.Model):
    ''' Add DOUBLE streamer field to a page. '''
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)
    
    end = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)

    panels = [
        StreamFieldPanel('body'),
        StreamFieldPanel('end'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True

class Streamer(models.Model):
    ''' Add SINGLE streamer field to a page. '''
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
    ], null=True, blank=True,)

    panels = [
        StreamFieldPanel('body'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True

class Seo(models.Model):
    ''' Add extra seo fields to pages such as icons. '''
    seo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        # default='media/images/default.png',
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional social media image 300x300px image < 300kb."
    )

    panels = [
        ImageChooserPanel('seo_image'),
    ]
    
    class Meta:
        """Abstract Model."""

        abstract = True