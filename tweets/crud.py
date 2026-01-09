from core.db_settings import execute_query

page_size = 5


def add_new_tweet(user):
    """
    New tweet adding function
    :param user:
    :return:
    """
    content = input("Write tweet here: ")

    query = "INSERT INTO tweets (user_id, tweet) VALUES (%s, %s)"
    execute_query(query, (user['id'], content))
    print("Tweet posted!")


def print_feed(user, page=0, order_by_likes=False):
    """
    Function to print all tweets
    :param user:
    :param page:
    :param order_by_likes:
    :return:
    """
    skip_amount = page * page_size

    # 1. Order part
    if order_by_likes:
        # Sort by Likes
        sql_order = "ORDER BY like_count DESC, t.created_at DESC"
        feed_title = "FEED (Order by likes)"
    else:
        # Sort by Date
        sql_order = "ORDER BY t.created_at DESC"
        feed_title = "FEED (Newest First)"

    print(f" {feed_title} - Page {page + 1} ")

    # 2. Group by to count likes. Limit and Offset to make page 1, page 2 ...
    query = f"""
        SELECT t.id, t.tweet, u.username, COUNT(l.id) as like_count
        FROM tweets t
        JOIN users u ON t.user_id = u.id
        JOIN likes l ON t.id = l.tweet_id
        GROUP BY t.id, u.username, t.created_at
        {sql_order}
        LIMIT %s OFFSET %s
    """

    tweets = execute_query(query, (page_size, skip_amount), fetch="all")

    if not tweets:
        print("No more tweets here.")
        return

    for t in tweets:
        print(f"[{t['id']}] {t['username']}: {t['tweet']}")
        print(f"    Likes: {t['like_count']}")


def print_my_tweets(user):
    """
    Prints only user's tweets
    :param user:
    :return:
    """

    query = "SELECT * FROM tweets WHERE user_id = %s ORDER BY created_at DESC"
    tweets = execute_query(query, (user['id'],), fetch="all")

    print(f" {user['username']}'s Tweets ")
    if not tweets:
        print("You haven't tweeted anything yet.")
    else:
        for t in tweets:
            print(f"[{t['id']}] {t['tweet']}")

def delete_tweet(user, tweet_id):
    """
    Deleting function to delete the tweet by their id
    :param user:
    :param tweet_id:
    :return:
    """
    # Check if the tweet belongs to the user
    check = "SELECT id FROM tweets WHERE id = %s AND user_id = %s"
    if execute_query(check, (tweet_id, user['id']), fetch="one"):
        # 2. Delete likes associated with the tweet
        execute_query("DELETE FROM likes WHERE tweet_id = %s", (tweet_id,))
        # 3. Delete the tweet
        execute_query("DELETE FROM tweets WHERE id = %s", (tweet_id,))
        print("Tweet deleted successfully.")
    else:
        print("Error: Tweet not found")