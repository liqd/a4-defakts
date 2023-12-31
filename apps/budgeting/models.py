from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.comments import models as comment_models
from adhocracy4.ratings import models as rating_models
from apps.mapideas import models as mapidea_models


class Proposal(mapidea_models.AbstractMapIdea):
    ratings = GenericRelation(
        rating_models.Rating,
        related_query_name="budget_proposal",
        object_id_field="object_pk",
    )
    comments = GenericRelation(
        comment_models.Comment,
        related_query_name="budget_proposal",
        object_id_field="object_pk",
    )
    budget = models.PositiveIntegerField(default=0, help_text=_("Required Budget"))

    is_archived = models.BooleanField(
        default=False,
        verbose_name=_("Proposal is archived"),
        help_text=_(
            "Exclude this proposal from all listings by default. "
            "You can still access this proposal by using filters."
        ),
    )

    def get_absolute_url(self):
        return reverse(
            "a4_candy_budgeting:proposal-detail",
            kwargs=dict(
                organisation_slug=self.project.organisation.slug,
                pk="{:05d}".format(self.pk),
                year=self.created.year,
            ),
        )

    class Meta:
        ordering = ["-created"]
