from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from apps.debate import phases as debate_phases
from apps.documents import phases as documents_phases
from apps.topicprio import phases as topicprio_phases

blueprints = [
    (
        "text-review",
        ProjectBlueprint(
            title=_("Text Review"),
            description=_(
                "Participants can discuss the paragraphs of a text that you "
                "added beforehand."
            ),
            content=[
                documents_phases.CommentPhase(),
            ],
            image="images/text-review.svg",
            settings_model=None,
            type="TR",
        ),
    ),
    (
        "topic-prioritization",
        ProjectBlueprint(
            title=_("Prioritization"),
            description=_(
                "Participants can discuss and rate (pro/contra) previously "
                "added ideas and topics. Participants cannot add ideas or "
                "topics."
            ),
            content=[
                topicprio_phases.PrioritizePhase(),
            ],
            image="images/priorization.svg",
            settings_model=None,
            type="TP",
        ),
    ),
    (
        "debate",
        ProjectBlueprint(
            title=_("Debate"),
            description=_(
                "Participants can discuss posted topics or questions. "
                "To do this, the participants comment on posted "
                "topics / questions as well as on contributions from other "
                "users."
            ),
            content=[
                debate_phases.DebatePhase(),
            ],
            image="images/debate.svg",
            settings_model=None,
            type="DB",
        ),
    ),
]
