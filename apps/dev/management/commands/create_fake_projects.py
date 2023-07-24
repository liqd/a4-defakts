import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from adhocracy4.comments.models import Comment
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.reports.models import Report
from apps.ai_reports.models import AiReport
from apps.debate.models import Subject
from apps.organisations.models import Member
from apps.organisations.models import Organisation
from apps.projects.models import Project
from apps.users.models import User


class Command(BaseCommand):
    help = "Creates fake projects and user activity"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            default=False,
            help="remove all fake data",
        )
        parser.add_argument(
            "--create",
            action="store_true",
            default=False,
            help="remove all fake data",
        )
        parser.add_argument(
            "--admin",
            action="store_true",
            default="admin@liqd.net",
            help="admin email to add to organisation",
        )

    def handle(self, *args, **options):
        if options["clean"]:
            remove_fake_data()
            return

        if options["create"]:
            remove_fake_data()

            now = timezone.now()
            start_time = now - timedelta(days=10)
            end_time = now + timedelta(days=10)
            email = options["admin"]
            n_users = 10
            n_comments = 20
            n_reports = 5
            n_ai_reports = 5

            admin = User.objects.filter(email=email).first()
            organisation = Organisation(name="fake_organisation")
            organisation.save()
            organisation.initiators.add(admin.id)

            users = []
            for i in range(n_users):
                username = f"fake_user_{i:03}"
                user = User(
                    username=username,
                    email=f"{username}@liqd.net",
                    password="pbkdf2_sha256$260000$wgsMj0aUgyuXixB9Pcei2w$TjwY6mVBu6yvLsV9rD/K8NQNHx46NJOPWJTRlrpxyFM=",  # for password "1234"
                )

                users.append(user)
                user.save()

            print(f"created users: {len(users)=}")

            member = Member(
                member=admin,
                organisation=organisation,
            )
            member.save()

            project = Project(
                name="fake_project",
                organisation=organisation,
                description="fake_description",
                information="fake_information",
                is_draft=False,
            )
            project.save()
            project.moderators.add(admin)

            module = Module(
                name="fake_debate",
                description="fake_description",
                project=project,
                weight=1,
                is_draft=False,
            )
            module.save()
            phase = Phase(
                type="a4_candy_debate:debate",
                module=module,
                name="fake_phase",
                description="fake_description",
                start_date=start_time,
                end_date=end_time,
            )
            phase.save()

            subject = Subject(
                name="fake_subject",
                module=module,
                creator=admin,
                description="fake_description",
                slug="fake_slug",
            )
            subject.save()

            comments = []
            for i in range(n_comments):
                comment = Comment(
                    comment=f"fake_comment_{i:03}",
                    content_object=subject,
                    creator=random.choice(users),
                    project=project,
                )
                comments.append(comment)

            Comment.objects.bulk_create(comments)
            comments = list(Comment.objects.filter(comment__startswith="fake_"))
            print(f"created comments: {len(comments)=}")

            size = min(n_reports, len(comments))
            comments_sample = random.sample(comments, size)
            reports = []
            for comment in comments_sample:
                report = Report(
                    creator=random.choice(users),
                    content_object=comment,
                    description="fake_report",
                )
                reports.append(report)

            Report.objects.bulk_create(reports)
            reports = Report.objects.filter(description__startswith="fake_")
            print(f"created reports: {len(reports)=}")

            size = min(n_ai_reports, len(comments))
            comments_sample = random.sample(comments, size)
            ai_reports = []
            for comment in comments_sample:
                ai_report = AiReport(
                    comment=comment,
                    explanation="fake_ai_report",
                )
                ai_reports.append(ai_report)

            AiReport.objects.bulk_create(ai_reports)
            ai_reports = AiReport.objects.filter(explanation__startswith="fake_")
            print(f"created ai_reports: {len(ai_reports)=}")


def remove_fake_data():
    """
    deleted, _rows_count = Organisation.objects.filter(name="fake_organisation").delete()
    print(f"deleted organisation: {_rows_count}")
    """

    models = [
        (Organisation, "name"),
        (Project, "name"),
        (User, "username"),
        (Project, "name"),
        (Comment, "comment"),
        (Module, "name"),
        (Subject, "name"),
    ]

    for model, key in models:
        deleted, _rows_count = model.objects.filter(
            **{f"{key}__startswith": "fake_"},
        ).delete()

        if _rows_count:
            print(f"deleted: {_rows_count}")
