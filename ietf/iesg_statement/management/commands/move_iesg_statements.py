from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from wagtail.contrib.redirects.models import Redirect

from ietf.blog.models import BlogPage
from ietf.iesg_statement.models import (
    IESGStatementIndexPage,
    IESGStatementPage,
    IESGStatementTopic,
)
from ietf.snippets.models import PrimaryTopic
from ietf.standard.models import StandardPage

slug_map = {
    "iesg-statement-maximizing-encrypted-access-ietf-information": "maximizing-encrypted-access",
    "iesg-statement-internet-draft-authorship": "internet-draft-authorship",
    "iesg-statement-designating-rfcs-historic": "designating-rfcs-historic-2014-07-20",
    "discuss-criteria-iesg-review": "iesg-discuss-criteria",
    "guidance-face-face-and-virtual-interim-meetings": "interim-meetings-guidance-2016-01-16",
    "writable-mib-module-iesg-statement": "writable-mib-module",
    "ietf-anti-harassment-policy": "anti-harassment-policy",
    "iesg-statement-removal-internet-draft-ietf-web-site": "internet-draft-removal",
    "iesg-statement-ethertypes": "ethertypes",
    "iesg-statement-designating-rfcs-historic-2011-10-20": "designating-rfcs-historic-2011-10-20",
    "iesg-statement-designating-rfcs-historic-2011-06-27": "designating-rfcs-historic-2011-06-27",
    "iesg-statement-iesg-processing-rfc-errata-concerning-rfc-metadata": "rfc-metadata-errata",
    "iesg-statement-document-shepherds": "document-shepherds",
    "iesg-statement-nomcom-eligibility-and-day-passes": "nomcom-eligibility-day-passes",
    "iesg-statement-usage-assignable-codepoints-addresses-and-names-specification-examples": "assignable-codepoints-addresses-names",
    "iesg-statement-copyright": "copyright-2009-09-08",
    "proposed-status-ietf-documents-reserving-resources-example-purposes": "reserving-resources-examples",
    "guidance-interim-meetings-conference-calls-and-jabber-sessions": "interim-meetings-guidance-2008-09-02",
    "iesg-processing-rfc-errata-ietf-stream": "processing-rfc-errata",
    "iesg-statement-spam-control-ietf-mailing-lists": "spam-control-2008-04-14",
    "guidance-spam-control-ietf-mailing-lists": "spam-control-2006-01-09",
    "iesg-guidance-moderation-ietf-working-group-mailing-lists": "mailing-lists-moderation",
    "iesg-statement-registration-requests-uris-containing-telephone-numbers": "registration-requests-uris",
    "iesg-statement-rfc3406-and-urn-namespaces-registry-review": "urn-namespaces-registry",
    "advice-wg-chairs-dealing-topic-postings": "off-topic-postings",
    "appeals-iesg-and-area-director-actions-and-decisions": "appeals-actions-decisions",
    "experimental-specification-new-congestion-control-algorithms": "experimental-congestion-control",
    "guidance-area-director-sponsoring-documents": "area-director-sponsoring-documents",
    "last-call-guidance-community": "last-call-guidance",
    "iesg-statement-normative-and-informative-references": "normative-informative-references",
    "iesg-statement-disruptive-posting": "disruptive-posting",
    "iesg-statement-auth48-state": "auth48",
    "syntax-format-definitions": "syntax-format-definitions",
    "iesg-statement-idn": "idn",
    "copyright-statement-mib-and-pib-modules": "copyright-2002-11-27",
    "guidance-spam-control-ietf-mailing-lists-2002-03-13": "spam-control-2002-03-13",
    "design-teams": "design-teams",
    "guidelines-use-formal-languages-ietf-specifications": "formal-languages-use",
    "establishment-temporary-sub-ip-area": "sub-ip-area-2001-03-21",
    "plans-organize-sub-ip-technologies-ietf": "sub-ip-area-2000-11-20",
    "new-ietf-work-area": "sub-ip-area-2000-12-06",
    "guidance-interim-ietf-working-group-meetings-and-conference-calls": "interim-meetings-guidance-2000-08-29",
    "ietf-meeting-photography-policy": "meeting-photography-policy",
    "support-documents-ietf-working-groups": "support-documents",
    "license-file-open-source-repositories": "open-source-repositories-license",
}


class Command(BaseCommand):
    help = "Moves the iesg statements from the blog app to the iesg_statements app"

    def handle(self, *args, **options):
        if IESGStatementPage.objects.exists():
            print(
                "IESGStatementPages exist. This command has probably already been run."
            )
            print("Exiting without making any changes.")
            return

        iesg_page = StandardPage.objects.get(pk=1210)
        index_page = IESGStatementIndexPage(
            title="IESG Statements",
            slug="statements",
            url_path=iesg_page.url_path + "/statements/",
        )
        iesg_page.add_child(instance=index_page)
        iesg_page.save()
        for stmt in BlogPage.objects.filter(
            primary_topics__topic__title="IESG Statements"
        ):

            if stmt.slug in slug_map:
                new_slug = slug_map[stmt.slug]
            else:
                new_slug = (
                    stmt.slug[15:]
                    if stmt.slug.startswith("iesg-statement-")
                    else stmt.slug
                )

            new_page = IESGStatementPage(
                title=stmt.title,
                slug=new_slug,
                date_published=stmt.date_published,
                introduction=stmt.introduction,
                url_path=index_page.url_path + "/" + new_slug,
                draft_title=stmt.draft_title,
                owner=stmt.owner,
                seo_title=stmt.seo_title,
                live=stmt.live,
                has_unpublished_changes=stmt.has_unpublished_changes,
                show_in_menus=stmt.show_in_menus,
                search_description=stmt.search_description,
                go_live_at=stmt.go_live_at,
                expire_at=stmt.expire_at,
                expired=stmt.expired,
                locked=stmt.locked,
                first_published_at=stmt.first_published_at,
                last_published_at=stmt.last_published_at,
                latest_revision_created_at=stmt.latest_revision_created_at,
                live_revision=stmt.live_revision,
            )
            index_page.add_child(instance=new_page)
            # Intentionally not creating/publishing a new revision
            new_page.body = stmt.body
            new_page.save()
            for st in stmt.secondary_topics.all():
                IESGStatementTopic.objects.create(page=new_page, topic=st.topic)

            Redirect.objects.create(
                old_path=stmt.url[:-1] if stmt.url.endswith("/") else stmt.url,
                is_permanent=True,
                redirect_page=new_page,
            )

        BlogPage.objects.filter(primary_topics__topic__title="IESG Statements").delete()
        PrimaryTopic.objects.filter(title="IESG Statements").delete()

        # todo - make this robust in case the iesg page gets edited before this is run on production
        iesg_page.key_info[6].value.source = (
            '<p><a href="statements">List\xa0All</a>\xa0\xa0| \xa0<a href="statements/?topic=20">On\xa0Mailing\xa0Lists</a>\xa0|\xa0<a href="statements?topic=21">On\xa0Meetings</a>\xa0|\xa0<a href="statements?topic=22">On\xa0Procedures</a>\xa0|\xa0<a href="statements?topic=23">On\xa0Technical\xa0Issues</a></p>'
        )
        iesg_page.save_revision(
            user=User.objects.get(username="robert.sparks")
        ).publish()
