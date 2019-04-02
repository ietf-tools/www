from django import template

from ietf.datatracker import models

register = template.Library()


@register.simple_tag
def person_area_role(person, area):
    try:
        groups = models.WorkingGroup.objects.filter(parent=area.resource_uri, active=True)
        roles = models.Role.objects.filter(
            person=person.resource_uri,
            group__in=groups.values_list('resource_uri', flat=True),
            active=True
        )
        return models.RoleName.objects.filter(
            resource_uri__in=roles.values_list('name', flat=True), active=True
        ).first().name
    except AttributeError:
        return ""
