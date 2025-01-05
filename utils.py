import os

from django.template.defaultfilters import slugify


def create_custom_path(instance, filename, base_dir):
    _, ext = os.path.splitext(filename)
    ext = ext.lower().strip(".")
    
    if hasattr(instance, "email"):
        return f"{base_dir}/{slugify(instance.email)}/profile.{ext}"
    elif hasattr(instance, "title"):
        return f"{base_dir}/{slugify(instance.title)}/image.{ext}"
    else:
        return f"{base_dir}/unknown.{ext}"
