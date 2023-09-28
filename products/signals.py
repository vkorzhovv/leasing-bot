# from django.db.models.signals import post_save, pre_save, post_delete
# from django.dispatch import receiver
# from .models import ProductMedia
# from urllib.parse import urlencode
# import io
# from django.conf import settings
# import os
# import json
# from django.utils.safestring import mark_safe
# from urllib.parse import urlparse, unquote
# import requests
# from django.core.files import File


# @receiver(post_save, sender=ProductMedia)
# def product_created(sender, instance, created, **kwargs):
#     if created:
#         if instance.media_url:
#             base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
#             public_key = instance.media_url

#             final_url = base_url + urlencode(dict(public_key=public_key))
#             response = requests.get(final_url)
#             download_url = response.json()['href']
#             parsed_url = urlparse(download_url)
#             filename = unquote(parsed_url.query.split("&filename=")[1].split("&")[0])

#             download_response = requests.get(download_url)
#             file_content = download_response.content


#             temp_file = File(io.BytesIO(file_content), name=filename)
#             instance.media = temp_file

#         instance.absolute_media_path = instance.get_absolute_media_path()