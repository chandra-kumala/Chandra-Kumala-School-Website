from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class Index(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        items = self.get_children().live().order_by('-first_published_at')
        context['items'] = items
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class itemTag(TaggedItemBase):
    content_object = ParentalKey(
        'item',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class item(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=itemTag, blank=True)
    categories = ParentalManyToManyField('items.itemCategory', blank=True)


    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="item information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class itemGalleryImage(Orderable):
    page = ParentalKey(item, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class itemTagIndex(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        items = item.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['items'] = items
        return context

@register_snippet
class itemCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        # FieldPanel('slug'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = "item Category"
        verbose_name_plural = "item categories"



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