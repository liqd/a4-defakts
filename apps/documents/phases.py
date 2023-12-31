from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class CommentPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "comment"
    view = views.DocumentDetailView

    name = _("Comment phase")
    module_name = _("commenting text")
    description = _("Post comments on the paragraphs of the text")

    features = {
        "comment": (models.Paragraph, models.Chapter),
    }


phases.content.register(CommentPhase())
