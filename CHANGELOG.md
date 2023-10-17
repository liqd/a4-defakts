# Changelog

All notable changes to this project will be documented in this file.

Since version v2310.1 the format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
This project (not yet) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v2310.1

### Added

- support for celery task queues with a redis message broker
- makefile commands for starting and status checking of celery worker processes
- ai_report field to dashboard moderation comments serializer
- userdashboard: added field "user_reports" to moderation comment serializer
- Ai report serializer for comments viewset (#7571)
- general switch button react component
- switch button to AIreportExplanation component
- show_in_discussion field to AiReport model
- component to show AiReport in userdashboard and a toggle to show/hide
  the report in the discussion
- react component to show AI report with dummy data for now
- new filter category for comments in moderator dashboard: "reported by ai"
- project insight model, create insight function,
  update insights with signals (#2492)
- pyenv file and vim backup extension in gitignore
- in contrib templates for item_detail:
    request http referer for go back/overview to filtered/paginated list
- in topicprio templates for topic_detail:
    request http referer for go back/overview to filtered/paginated list
- in budgeting, idea, mapidea, topicprio:
    index id to be used with href anchor to navigate back to item list
- in contrib templates for map_filter_and_sort and pagination:
    index id to be used with href anchor to navigate back to item list


### Changed

- ai_report field from StringRelatedField to AiReportSerializer in
  CommentWithFeedbackSerializer
- brand-alert color to match the design
- structure of ModerationNotification to be more a11y compliant
- fix tests which included removed modules
- update a4 to 208d5c1134da702fc5c6e8c5c8ea8d55ac2d012d
- update a4 to 73ad60e06a557dbd00e7a1118fb639d13e8b4244
- only english and german language options

### Fixed

- fix broken pytest-lastfailed command in Makefile

### Removed

- modules brainstorming, map-brainstorming, idea-collection,
  map-idea-collection, poll, participatory-budgeting, interactive-event and
  associated tests
- frontend coverage ci actions
- unused language translations from locale fork
