import requests
from config import AUTH_TOKEN, FOLLOW_CHECK_USER

# Headers for authorization and accepting GitHub API format
headers = {
    'Authorization': f'token {AUTH_TOKEN}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Accept': 'application/vnd.github+json'
}

def is_following(target_user, followed_user):
    """
    Check if `target_user` is following `followed_user`.
    """
    try:
        response = requests.get(f'https://api.github.com/users/{target_user}/following/{followed_user}', headers=headers)
        return response.status_code == 204
    except requests.RequestException as error:
        print(f"Error checking if user {target_user} is following {followed_user}: {error}")
        return False

def unfollow_user(target_user):
    """
    Unfollow the specified `target_user`.
    """
    try:
        response = requests.delete(f'https://api.github.com/user/following/{target_user}', headers=headers)
        if response.status_code == 204:
            print(f'User {target_user} has been unfollowed successfully.')
        else:
            print(f'Failed to unfollow user {target_user}. Status code: {response.status_code}. Response: {response.text}')
    except requests.RequestException as error:
        print(f"Error unfollowing user {target_user}: {error}")

def get_following_list():
    """
    Retrieve the list of users that the authenticated user is following.
    Iterates through all pages of results.
    """
    following_list = []
    page = 1
    while True:
        try:
            response = requests.get('https://api.github.com/user/following', headers=headers, params={'per_page': 100, 'page': page})
            response.raise_for_status()
            current_page_followings = response.json()

            if not current_page_followings:
                break

            following_list.extend([user['login'] for user in current_page_followings])
            page += 1
        except requests.RequestException as error:
            print(f"Error retrieving following list: {error}")
            break
    
    return following_list

def process_followers():
    """
    Process the list of users followed by the authenticated user.
    Check if each user follows `FOLLOW_CHECK_USER` and unfollow them if they do not.
    """
    followed_users = get_following_list()
    print(followed_users)

    for user in followed_users:
        if is_following(user, FOLLOW_CHECK_USER):
            print(f'{user} is following {FOLLOW_CHECK_USER}.')
        else:
            print(f'{user} is not following {FOLLOW_CHECK_USER}. Unfollowing...')
            unfollow_user(user)

if __name__ == "__main__":
    process_followers()
