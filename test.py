def preprocess_json_data(data):
    new_data = {}
    for subreddit, posts in data.items():
        new_data[subreddit] = []
        
        for post in posts:
            # Check the number of comments at depth=0
            comments_depth_0 = [comment for comment in post['comments'] if comment['depth'] == 0]

            if comments_depth_0:
                for i, comment in enumerate(comments_depth_0):
                    # Create a new post with metadata including comment index
                    new_post = {
                        'title': post['title'],
                        'author': post['author'],
                        'id': post['id'],
                        'permalink': post['permalink'],
                        'selftext': post['selftext'],
                        'comments': [comment],  # Only include the comment at depth=0
                        'comment_body': comment['body'],
                        'comment_index': i,  # Add the comment index
                        'thumbnail': post['thumbnail'],
                        'thumbnail_width': post['thumbnail_width']
                    }
                    new_data[subreddit].append(new_post)

    return new_data
dummy_data = {
    "DermApp": [
        {
            "title": "Post about a mole",
            "author": "user1",
            "id": "abc123",
            "permalink": "/r/DermApp/post_about_a_mole",
            "selftext": "What do you think about this mole?",
            "thumbnail": "url_to_thumbnail",
            "thumbnail_width": 100,
            "comments": [
                {
                    "id": "def456",
                    "author": "doctor1",
                    "body": "It looks benign, but you should get it checked.",
                    "score": 5,
                    "subreddit": "DermApp",
                    "depth": 0
                },
                {
                    "id": "xyz890",
                    "author": "AutoModerator",
                    "body": "Automated response.",
                    "score": 1,
                    "subreddit": "DermApp",
                    "depth": 0
                },
                {
                    "id": "def457",
                    "author": "doctor2",
                    "body": "It looks bad, but you should get it checked.",
                    "score": 2,
                    "subreddit": "DermApp",
                    "depth": 0
                },
            ]
        },
        # Other posts...
    ],
    "DermatologyQuestions": [
        # Posts for DermatologyQuestions...
    ]
    # Other subreddits...
}



import random
data = preprocess_json_data(dummy_data)
# Sample data dictionary

def load_random_post(selected_subreddit, userID):
    if selected_subreddit in data:
        all_posts = data[selected_subreddit]
        if all_posts:
            # Filter out posts with no comments and specific authors
            valid_posts = [
                post for post in all_posts
                if post.get('comments') != "[Removed]"  # Check if comments are not "[Removed]"
                and post.get('comments') and not all(comment['author'] == 'AutoModerator' or comment['author'] == 'None' for comment in post['comments'])
                and (userID, post.get('id'), post.get('comment_index')) not in session_state._state
            ]
            invalid_posts = [
                post for post in all_posts
                if post.get('comments') != "[Removed]"  # Check if comments are not "[Removed]"
                and post.get('comments') and not all(comment['author'] == 'AutoModerator' or comment['author'] == 'None' for comment in post['comments'])
                and (userID, post.get('id'), post.get('comment_index'))  in session_state._state
            ]
            
            if valid_posts:

                # Should I add functionality here to add the random_post to a list and to choose a different choice if the valid post has already been shown?

                random_post = random.choice(valid_posts)
                return random_post
    return None

# Dummy session state
class SessionState:
    def __init__(self, ):
        self._state = {}

    def get(self, key, default):
        return self._state.get(key, default)

    def set(self, key, value):
        self._state[key] = value

    def delete(self, key):
        if key in self._state:
            del self._state[key]

# Create an instance of the session state
import random

# Sample data dictionary
# data = {
#     'subreddit_1': [
#         {
#             'id': '1',
#             'comment_index': 0,
#             'comments': [{'author': 'User1'}, {'author': 'User2'}]
#         },
#         {
#             'id': '2',
#             'comment_index': 0,
#             'comments': [{'author': 'User3'}, {'author': 'User4'}]
#         }
#     ],
#     'subreddit_2': [
#         {
#             'id': '3',
#             'comment_index': 0,
#             'comments': [{'author': 'User5'}, {'author': 'User6'}]
#         }
#     ]
# }

# Dummy session object


# Create an instance of the SessionState class
session_state = SessionState()

# # Sample userID
userID = 'User1'

# # Add a post to the session state
# session_state.set((userID, '1', 0), True)

# # Call the load_random_post function
# random_post = load_random_post('subreddit_1', userID)

# # Check if the post in session state is ignored
# if random_post is None:
#     print("True")  # It should print True as the post is ignored
# else:
#     print("False")

# Output will be True because the post in session state was ignored.
def test_load_random_post():
    # Preprocess the data
    preprocessed_data = preprocess_json_data(dummy_data)

    # Create a session state instance
    session_state = SessionState()

    # Scenario 1: Test for a random post selection
    random_post = load_random_post('DermApp', 'user_test')
    assert random_post is not None, "Failed to load a random post."

    # Scenario 2: Test for filtering out 'AutoModerator' and 'None'
    assert all(comment['author'] not in ['AutoModerator', 'None'] for comment in random_post['comments']), "Post with AutoModerator or None author should be filtered out."

    # Scenario 3: Test for ignoring posts already in session state
    session_key = ('user_test', random_post['id'], random_post['comment_index'])
    session_state.set(session_key, True)
    new_random_post = load_random_post('DermApp', 'user_test')
    new_session_key = (new_random_post['id'], new_random_post['comment_index'])
    assert session_key != new_session_key, "Should not select a comment already in session state."
    
    print("All tests passed.")

# Run the test function
test_load_random_post()



def main():
    output=preprocess_json_data(dummy_data)
    # print(output)/
    data=output
    random_post = load_random_post('DermApp', userID)
    print(random_post)
    
    
    return
if __name__ == '__main__':
    main()
    