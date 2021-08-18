from src.users.enums import Action
from src.users.exceptions import InvalidFollowEvent


def validate_follow_event(follow_event, meta):
    """
    Validates a follow_event.
    Raises for invalid follow_event.
    """
    reasons = get_reasons_follow_event_invalid(follow_event)
    if reasons:
        raise InvalidFollowEvent(f'{reasons[0]} meta: {str(meta)}')


def get_reasons_follow_event_invalid(follow_event):
    """
    Returns reasons a follow_event is invalid.
    """
    reasons = []
    action = follow_event['action']
    if action not in [action.value for action in Action]:
        reasons.append(f"Unknown action: '{action}'.")
    return reasons or None


def get_users_from_user_follower_mapping(user_follower_mapping):
    """
    Returns a list of the superset of users from user_follower_mapping.
    """
    users = set()
    for user, followers in user_follower_mapping.items():
        users.add(user)
        for follower in followers:
            users.add(follower)
    return list(users)


def build_user_follower_mapping(follow_event, user_follower_mapping=None):
    """
    Builds a mapping of users and who they follow based on a follow_event.
    Returns a new dictionary of user to followers.
    """
    new_user_follower_mapping = dict(user_follower_mapping or {})
    user = follow_event['user']
    followers = set(new_user_follower_mapping.get(user, []))
    for follower in follow_event['followers']:
        action = follow_event['action']
        if action == Action.FOLLOWS.value:
            followers.add(follower)
        elif action == Action.UNFOLLOWS.value:
            followers.remove(follower)
        else:
            raise Exception(f'Unknown action: {action}.')
    new_user_follower_mapping[user] = list(followers)
    return new_user_follower_mapping


def build_user_follower_mapping_for_multiple_follow_events(follow_events, user_follower_mapping=None):
    """
    Builds a mapping of users and who they follow based on follow_events.
    Returns a new dictionary of user to followers.
    """
    new_user_follower_mapping = dict(user_follower_mapping or {})
    for follow_event in follow_events:
        new_user_follower_mapping = {
            **new_user_follower_mapping,
            **build_user_follower_mapping(
                follow_event,
                new_user_follower_mapping,
            )
        }
    return new_user_follower_mapping
