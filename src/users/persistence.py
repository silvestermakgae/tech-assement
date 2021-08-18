from src import utils
from src.users.enums import Action
from src.users.exceptions import InvalidFollowEventLine


def validate_follow_event_line(follow_event_line, meta):
    reasons = get_reasons_follow_event_line_invalid(follow_event_line)
    if reasons:
        raise InvalidFollowEventLine(f'{reasons[0]} meta: {str(meta)}')


def get_reasons_follow_event_line_invalid(follow_event_line):
    reasons = []
    action = follow_event_line.split(' ')[1]
    if action not in [action.value for action in Action]:
        reasons.append(f"Unknown action: '{action}'.")
    return reasons or None


def parse_follow_event_line(follow_event_line):
    user, action, _followers = (
        follow_event_line
        # For simpler splitting of followers below.
        .replace(', ', ',')
        .split(' ')
    )
    # TODO: Should this assertion be here if we are validating separately elsewhere?
    assert action in [action.value for action in Action]
    followers = _followers.split(',')
    return {
        'user': user,
        'action': action,
        'followers': followers,
    }


def parse_follow_event_file(path, line_cb=None, follow_event_cb=None):
    follow_events_file = utils.read_text_file(path)
    follow_events = []
    for index, line in enumerate(follow_events_file):
        meta = {
            'line_number': index + 1,
        }
        if line_cb:
            line_cb(line, meta=meta)
        follow_event = parse_follow_event_line(line.strip('\n'))
        if follow_event_cb:
            follow_event_cb(follow_event, meta)
        follow_events.append(follow_event)
    return follow_events
