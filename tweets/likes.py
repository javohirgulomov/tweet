from core.db_settings import execute_query


def toggle_like(user, tweet_id):
    """
    Handles liking and unliking a tweet.
    """
    # Is tweet exists ?
    if not execute_query("SELECT id FROM tweets WHERE id = %s", (tweet_id,), fetch="one"):
        print("Error: Tweet not found.")
        return

    # Did user already liked this tweet?
    check_query = "SELECT id FROM likes WHERE user_id = %s AND tweet_id = %s"
    existing_like = execute_query(check_query, (user['id'], tweet_id), fetch="one")

    if existing_like:
        # If user already liked that tweet, unlike the tweet
        execute_query("DELETE FROM likes WHERE user_id = %s AND tweet_id = %s", (user['id'], tweet_id))
        print("Unliked")
    else:
        # If user did not like that tweet, operate liking function
        execute_query("INSERT INTO likes (user_id, tweet_id) VALUES (%s, %s)", (user['id'], tweet_id))
        print("Liked!")


def show_liked_tweets(user):
    """
    Shows tweets the user liked
    """
    query = """
            SELECT t.tweet, u.username
            FROM likes l
            JOIN tweets t ON l.tweet_id = t.id
            JOIN users u ON t.user_id = u.id
            WHERE l.user_id = %s 
            """
    tweets = execute_query(query, (user['id'],), fetch="all")

    print("Tweets You Liked")
    if not tweets:
        print("You haven't liked anything yet.")
    else:
        for t in tweets:
            print(f"{t['username']}: {t['tweet']}")

def show_who_liked_tweet(user, tweet_id):
    """
    Shows the list of users who liked that tweet
    :param user:
    :param tweet_id:
    :return:
    """

    #Is this your tweet?
    check = "SELECT id FROM tweets WHERE id = %s AND user_id = %s"
    if not execute_query(check, (tweet_id, user['id']), fetch="one"):
        print("This is not your tweet")
        return
    query = """
        SELECT u.username FROM likes l JOIN users u ON l.user_id = u.id
        WHERE l.tweet_id = %s
    """
    likers = execute_query(query, (tweet_id,), fetch="all")
    print("Users who liked this tweet: ")
    if not likers:
        print("No likes")
    else:
        for liker in likers:
            print(f"{liker['username']}")
