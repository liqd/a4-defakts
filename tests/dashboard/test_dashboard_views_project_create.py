import pytest
from django.conf import settings
from django.contrib.messages import get_messages
from django.urls import reverse

from adhocracy4.modules.models import Module
from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_project_create(client, organisation, user):
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:project-create",
        kwargs={
            "organisation_slug": organisation.slug,
        },
    )

    data = {"name": "project name", "description": "project description", "access": 1}

    response = client.post(url, data)
    assert redirect_target(response) == "account_login"

    client.login(username=user, password="password")
    response = client.post(url, data)
    assert response.status_code == 403

    client.login(username=initiator, password="password")
    response = client.post(url, data)
    assert redirect_target(response) == "project-edit"

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert "project name" == project.name
    assert "project description" == project.description


@pytest.mark.django_db
def test_module_blueprint_list(client, project):
    organisation = project.organisation
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:module-blueprint-list",
        kwargs={"organisation_slug": organisation.slug, "project_slug": project.slug},
    )
    client.login(username=initiator.email, password="password")
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ["a4_candy_dashboard/module_blueprint_list.html"]

    brainstorming_url = reverse(
        "a4dashboard:module-create",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
            "blueprint_slug": "topic-prioritization",
        },
    )

    assert brainstorming_url in response.content.decode()

    blueprint_names = [b[0] for b in response.context_data["view"].blueprints]
    assert "text-review" in blueprint_names
    assert "topic-prioritization" in blueprint_names

    blueprint_types = [b[1][5] for b in response.context_data["view"].blueprints]
    settings_blueprint_types = [b[0] for b in settings.A4_BLUEPRINT_TYPES]
    for blueprint_type in blueprint_types:
        assert blueprint_type in settings_blueprint_types


@pytest.mark.django_db
def test_module_create(client, project):
    organisation = project.organisation
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:module-create",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
            "blueprint_slug": "debate",
        },
    )
    client.login(username=initiator.email, password="password")

    response = client.post(url)

    assert redirect_target(response) == "dashboard-module_basic-edit"
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "The module was created"

    response2 = client.post(response.url)
    assert not response2.context_data["form"].is_valid()
    assert "name" in response2.context_data["form"].errors
    assert "description" in response2.context_data["form"].errors

    data = {"name": "debate module", "description": "debate chosen topics"}

    response3 = client.post(response.url, data)

    assert response3.status_code == 302
    response4 = client.get(response3.url)
    assert response4.context_data["form"].errors == {}

    assert Module.objects.all().count() == 1
    module = Module.objects.first()
    assert module.name == data["name"]
    assert module.description == data["description"]
    assert module.blueprint_type == "DB"


@pytest.mark.django_db
def test_module_delete(client, module_factory):
    module1 = module_factory()
    project = module1.project
    module2 = module_factory(project=project, is_draft=True)
    organisation = project.organisation
    initiator = organisation.initiators.first()

    assert project.modules.count() == 2

    url = reverse(
        "a4dashboard:module-delete",
        kwargs={"organisation_slug": organisation.slug, "slug": module1.slug},
    )
    client.login(username=initiator.email, password="password")

    response = client.post(url)
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert (
        str(messages[-1]) == "Module cannot be deleted. It has to be "
        "removed from the project first."
    )
    assert redirect_target(response) == "project-edit"
    assert project.modules.count() == 2

    url = reverse(
        "a4dashboard:module-delete",
        kwargs={"organisation_slug": organisation.slug, "slug": module2.slug},
    )
    response = client.post(url)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[-1]) == "The module has been deleted"
    assert project.modules.count() == 1
