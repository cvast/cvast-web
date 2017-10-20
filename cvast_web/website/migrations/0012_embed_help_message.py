# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-20 16:00
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_background_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock())])), ('image_header_left', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=300)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True))])), ('page_wide_image', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=300)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True))])), ('embed_video', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=300)), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='This URL must be an embed URL, e.g. https://www.youtube.com/embed/6wr0PWi9LXQ'))]))]),
        ),
    ]
