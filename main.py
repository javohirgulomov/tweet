from auth import login
from core import models
from core.db_settings import execute_query
from utils import menus
from tweets import crud, likes



def show_auth_menu():
    """
    Main menu page
    :return:
    """
    print(menus.auth_menu)
    option = input("Enter your option: ")

    if option == "1":
        user = login.login()
        if user:
            print(f"Welcome back, {user['username']}!")
            return show_main_menu(user)
        else:
            return show_auth_menu()

    elif option == "2":
        if login.register():
            print("Registration successful! Please login.")
        return show_auth_menu()

    elif option == "3":
        print("Goodbye!")
        return None

    return show_auth_menu()


def show_all_tweets_menu(user, page=0, sort_by_likes=False):
    """
    All tweets and functions menu
    :param user:
    :param page:
    :param sort_by_likes:
    :return:
    """
    # sort_by_likes function
    crud.print_feed(user, page, order_by_likes=sort_by_likes)

    print(menus.all_tweets_menu)
    option = input("Enter your option: ")

    if option == "0":  # Back
        return show_main_menu(user)

    elif option == "1":  # Next Page
        return show_all_tweets_menu(user, page + 1, sort_by_likes)

    elif option == "2":  # Previous Page
        if page > 0:
            return show_all_tweets_menu(user, page - 1, sort_by_likes)
        else:
            print("You are already on the first page.")
            return show_all_tweets_menu(user, page, sort_by_likes)

    elif option == "3":  # Like
        tweet_id = input("Enter Tweet ID to Like: ")
        likes.toggle_like(user, int(tweet_id))
        return show_all_tweets_menu(user, page, sort_by_likes)

    elif option == "4":  # Unlike
        tweet_id = input("Enter Tweet ID to Unlike: ")
        likes.toggle_like(user, int(tweet_id))
        return show_all_tweets_menu(user, page, sort_by_likes)

    elif option == "5":  # Order by likes
        print("Sorting by popularity...")
        # We set sort_by_likes=True
        return show_all_tweets_menu(user, page=0, sort_by_likes=True)

    else:
        return show_all_tweets_menu(user, page, sort_by_likes)


def show_my_tweets_menu(user):
    """
    User tweets section
    :param user:
    :return: tweets
    """

    crud.print_my_tweets(user)

    print(menus.my_tweet_menu)
    option = input("Enter your option: ")

    if option == "1":  # Delete
        tweet_id = input("Enter Tweet ID to delete: ")
        crud.delete_tweet(user, int(tweet_id))
        return show_my_tweets_menu(user)

    elif option == "2":  # Show liked users
        tweet_id = input("Enter Tweet ID to see who liked it: ")

        likes.show_who_liked_tweet(user, int(tweet_id))
        input("Press Enter to continue")
        return show_my_tweets_menu(user)

    elif option == "3":  # Back
        return show_main_menu(user)

    else:
        return show_my_tweets_menu(user)


def show_main_menu(user):
    """
    Heart of the program. Main menu
    :param user:
    :return: funtions
    """
    print(menus.main_menu)
    option = input("Enter your option: ")

    if option == "1":
        # Global Feed
        return show_all_tweets_menu(user)

    elif option == "2":
        # User tweet section
        return show_my_tweets_menu(user)

    elif option == "3":
        # Liked Tweets
        likes.show_liked_tweets(user)
        input("Press Enter to continue")
        return show_main_menu(user)

    elif option == "4":
        # Add Tweet
        crud.add_new_tweet(user)
        return show_main_menu(user)

    elif option == "5":
        # Logout
        print("Logging out")
        return show_auth_menu()

    else:
        print("Invalid option.")
        return show_main_menu(user)


if __name__ == '__main__':
    execute_query(query=models.users)
    execute_query(query=models.tweets)
    execute_query(query=models.likes)
    execute_query(query=models.codes)

    show_auth_menu()