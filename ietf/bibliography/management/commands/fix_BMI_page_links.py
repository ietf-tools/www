import re

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm
from wagtail.models import Page

from ietf.blog.models import BlogPage
from ietf.iesg_statement.models import IESGStatementPage
from ietf.snippets.models import RFC, Charter, WorkingGroup
from ietf.standard.models import StandardPage


def change_links(page):

    unfound_rfcs = set()

    rfc_pattern = re.compile("^ *\\[? *RFC *(\\d{4}) *\\]? *$")

    group_pattern1 = re.compile("\((\w+)\)\\xa0[Ww]orking [Gg]roup$")
    group_pattern2 = re.compile(" *(\w+) +[Ww]orking [Gg]roup$")

    for fieldname in page.CONTENT_FIELD_MAP.keys():
        field = getattr(page, fieldname)
        for item in field.stream_data:
            if not item["type"] in ("paragraph", "raw_html"):
                continue
            soup = BeautifulSoup(item["value"], "html.parser")
            for tag in soup.find_all("a", string=rfc_pattern):
                if "href" in tag.attrs:
                    continue
                rfc_number = rfc_pattern.match(tag.string)[1]
                rfc = RFC.objects.filter(rfc=rfc_number).first()
                if not rfc:
                    unfound_rfcs.add(rfc_number)
                    continue
                tag["data-app"] = "snippets"
                tag["data-linktype"] = "rfc"
                tag["data-id"] = str(rfc.pk)
            for pattern in (group_pattern1, group_pattern2):
                for tag in soup.find_all("a", string=pattern):
                    if "href" in tag.attrs:
                        continue
                    if "linktype" in tag.attrs and tag["linktype"] != "charter":
                        continue
                    if not pattern.search(tag.string):
                        print("Search failure", tag.string, pattern)
                        print(page.url_path)
                        continue
                    acronym = pattern.search(tag.string)[1].lower()
                    charter = Charter.objects.filter(
                        working_group__acronym=acronym
                    ).first()
                    if charter:
                        tag["data-app"] = "snippets"
                        tag["data-linktype"] = "charter"
                        tag["data-id"] = str(charter.pk)
                    else:
                        group = WorkingGroup.objects.filter(acronym=acronym).first()
                        if group:
                            tag["data-app"] = "snippets"
                            tag["data-linktype"] = "workinggroup"
                            tag["data-id"] = str(group.pk)
                        else:
                            print("Nothing found in ", str(tag))
                            print("Acronym was", acronym)
                            continue
            item["value"] = str(soup)

    all_the_fields = list(page.CONTENT_FIELD_MAP.keys())
    all_the_fields.extend(list(page.CONTENT_FIELD_MAP.values()))
    page.save(update_fields=all_the_fields)

    return unfound_rfcs


class Command(BaseCommand):
    help = "Replace <a> tag parameters on pages using BibliographyMixin"

    def add_arguments(self, parser):
        parser.add_argument("url_paths", nargs="*", type=str)

    def handle(self, *args, **options):

        unfound_rfcs = set()

        if options["url_paths"]:
            for url_path in options["url_paths"]:
                page = Page.objects.filter(url_path=url_path).first()
                if not page:
                    CommandError("Page with path " + url_path + " not found")
                unfound_rfcs.update(change_links(page.specific))
        else:
            print("Standard Pages:")
            for page in tqdm(StandardPage.objects.all()):
                unfound_rfcs.update(change_links(page))
            print("Blog Pages:")
            for page in tqdm(BlogPage.objects.all()):
                unfound_rfcs.update(change_links(page))
            print("IESGStatement Pages:")
            for page in tqdm(IESGStatementPage.objects.all()):
                unfound_rfcs.update(change_links(page))
        if unfound_rfcs:
            print("Unfound RFCs", unfound_rfcs)
