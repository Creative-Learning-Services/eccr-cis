from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DjangoDomain, NeoDomain


@receiver(post_save, sender=DjangoDomain)
def create_neo_domain(sender, instance, created, **kwargs):
    """
    Create domain in Neo4j when Django one created
    """
    if created:
        NeoDomain.get_or_create({'uuid': instance.uuid.hex, 'name':
                                 instance.name})
