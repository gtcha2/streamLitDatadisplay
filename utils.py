def get_comments(data, subreddit, post_id):
    # Get the posts from the selected subreddit
    posts = data[subreddit]

    # Get the selected post
    post = next(post for post in posts if post['id'] == post_id)

    # Return the comments from the selected post
    return post['comments']

