# Mario

[![Build Status](https://travis-ci.org/best-doctor/Mario.svg?branch=master)](https://travis-ci.org/best-doctor/Mario)
[![Maintainability](https://api.codeclimate.com/v1/badges/86b3c0549c660bda7f4f/maintainability)](https://codeclimate.com/github/best-doctor/Mario/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/86b3c0549c660bda7f4f/test_coverage)](https://codeclimate.com/github/best-doctor/Mario/test_coverage)
[![PyPI version](https://badge.fury.io/py/super-mario.svg)](https://badge.fury.io/py/super-mario)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/super-mario)

Library for separating data input, output and processing in your business application.

![Mario](https://raw.githubusercontent.com/best-doctor/Mario/master/docs_imgs/mario.png)

**Disclaimer**: the library is sooo pre-alpha.

## Motivation & main idea

You have tons of business logic.
You like clean architecture, but you're sane. 
You like dynamic structure of Python, but you're tied of runtime errors.
You want to break things a little less and keep moving fast.
You're is the right place.

Mario is a framework for business logic.
Like Django or Flask for web-services.

It makes you put logic to pipelines: sets of pipes,
each pipe does only one thing and only non-complex types
can be transferred from pipe to pipe.

Each pipe is one of 3 types: input, output, processing.
Input and output should be non-complex (like really non-complex,
cyclomatic complexity ~3), processing pipes should be pure. 

## Installation

`pip install super-mario`

## Usage example

Here is simple pipeline, that send notifications on new comments in Jira
tickets to Slack. 

```python
class JiraCommentsNotificationPipeline(BasePipeline):
    pipeline = [
        'fetch_new_comments',
        'fetch_users_mapping',
        'generate_slack_message',
        'send_slack_message',
    ]

    @input_pipe
    def fetch_new_comments(jira_ticket_id: str) -> ImmutableContext:
        return {'new_comments':
            fetch_jira_comments(
                ticket_id=jira_ticket_id,
                date_from=datetime.datetime.now().replace(hours=0, minutes=0, seconds=0, milliseconds=0),
            ),
        }

    @input_pipe
    def fetch_users_mapping(new_comments: List[IssueComment]) -> ImmutableContext:
        return {
            'jira_to_slack_id_mapping': dict(User.objects.filter(
                jira_id__in=[c['user_id'] for c in new_comments],
            ).values_list('jira_id', 'slack_id'))
        }

    @process_pipe
    def generate_slack_message(
        jira_ticket_id: str,
        new_comments: List[IssueComment],
        jira_to_slack_id_mapping: Mapping[str, str],
    ) -> ImmutableContext:
        message = '\n'.join([
            f'@{jira_to_slack_id_mapping[c["user_id"]]} wrote comment for {jira_ticket_id}: "{c['text']}"'
            for c in new_comments
        ])
        return {'message': message}

    @output_pipe
    def send_slack_message(message: str) -> None:
        send_message(
            destination='slack',
            channel=COMMENTS_SLACK_CHANNEL_ID,
            text=message,
        )

# run pipeline for specific ticket
JiraCommentsNotificationPipeline().run(jira_ticket_id='TST-12')
``` 
