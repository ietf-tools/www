from django.db import transaction
from django.db.models.signals import post_init

from wagtail.search.management.commands.update_index import Command as WagtailCommand

from ietf.datatracker.models import DisconnectSignal, update_instance_receiver, DatatrackerMixin


class Command(WagtailCommand):
    @transaction.atomic
    def queryset_chunks(self, qs, chunk_size=1000):
        i = 0
        while True:
            if qs.model in DatatrackerMixin.__subclasses__():
                with DisconnectSignal(
                        signal=post_init, receiver=update_instance_receiver, sender=qs.model
                ):
                    items = list(qs[i * chunk_size:][:chunk_size])
            else:
                items = list(qs[i * chunk_size:][:chunk_size])
            if not items:
                break
            yield items
            i += 1
