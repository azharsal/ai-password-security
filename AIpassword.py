import json
import re
import os
from openai import OpenAI

# Load API key from environment variable for security
# Set your key: export OPENAI_API_KEY="your-key-here"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import requests
import itertools
import Levenshtein as lev
from datetime import datetime

posts_file_path = 'posts.json'  # Path to the JSON file where posts are stored
accounts_file_path = 'accounts.json'  # Path to the JSON file storing account details
curr_user = ""


def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding the JSON file: {file_path}.")
        return {}


# Can be passed the dictionary reagrding accounts of posts and saved to the specified file path. 
def save_json(data, file_path):
    """Save JSON data to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


# Function to generate basic combinations of keywords
def generate_basic_combinations(keywords, max_combination_length=2):
    combinations = []
    for r in range(1, max_combination_length + 1):
        for combo in itertools.combinations(keywords, r):
            combinations.append(''.join(combo))
    return combinations

# Function to apply common substitutions to simulate leet speak
def apply_leet_speak_substitutions(combinations):
    leet_substitutions = {
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'
    }
    leet_combinations = []
    for combo in combinations:
        leet_combo = combo
        for char, leet_char in leet_substitutions.items():
            leet_combo = leet_combo.replace(char, leet_char)
        leet_combinations.append(leet_combo)
    return leet_combinations

# Function to append/prepend common special characters and numbers
def append_special_characters_and_numbers(combinations):
    special_chars = ['!', '@', '#', '.', '?']
    numbers = ['123', '2024', '1']
    new_combinations = []
    for combo in combinations:
        for number in numbers:
            word_number = combo + number
            number_word = number + combo 
            for char in special_chars:
                new_combinations.append(word_number + char)
                new_combinations.append(char + word_number)
                new_combinations.append(number_word + char)
                new_combinations.append(char + number_word)

    return new_combinations


# Compare the list of concoted potential passwords to the password itself.
def compare_guesses(combinations, password, closeness_threshold=3):

    close = []
    for combo in combinations:
        # Check for an exact match
        if combo == password:
            print(f"Exact match found: {combo}")
            return True
        # Check for closeness based on the Levenshtein distance
        elif lev.distance(combo, password) <= closeness_threshold:
            close.append(combo)
    if len(close) > 0:
        print("These are the close matches found for your pasword:")
        print(close)
        return True
    else:
        print("No match or close match found.")
        return False

    # return False

def constant_password_strength_check(user_id, posts, password):
    # Ensure you have the user's posts loaded into the posts variable
    user_posts = posts["users"][user_id]["posts"]
    posts_content = [post["content"] for post in user_posts]

    data = {
    "family": ["mother", "father", "aunt", "uncle", "son", "daughter","brother",  "grandmother", "grandfather", "cousin", "niece", "nephew"],
    "hobbies": ["sports", "video games", "photography", "movies", "reading", "music", "cooking", "traveling", "painting", "gardening"],
    "event": ["anniversaries", "birthdays", "weddings", "graduations", "parties", "holidays", "concerts", "festivals", "reunions"]
    }

    prompt = f"""
    I'm providing you with a list of strings that contain various information. I need you to analyze these strings and extract terms related to specific categories: relationships, names, locations, events, dates, pets, and hobbies. 
    I'd like you to compile all extracted terms into a single list, regardless of their category. 
    Additionally, for any terms related to hobbies, please identify and include any associated names or terms if possible. 
    The final output should be in JSON format, consisting of a single list that includes all the terms you've identified, like this: 
    {{"mentioned": ["term1", "term2", "name1", "event1",...]}}. Find any hobbies or non-words, and analyze each one to find terms related to them 
    and include them alongside the hobby in the list. Can you do this analysis and provide the summarized output in the requested format? Here is the list:
    {', '.join(posts_content)}
    """     


    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON, which only has one key called mentioned and the results are simply one list of strings. "},
        {"role": "user", "content": prompt}
    ])

    # keywords =
    parsed_json = json.loads(response.choices[0].message.content)

    # Extract the "mentioned" list
    keywords = parsed_json["mentioned"]

    basic_combinations = generate_basic_combinations(keywords)
    leet_combinations = apply_leet_speak_substitutions(basic_combinations)
    final_combinations = append_special_characters_and_numbers(basic_combinations + leet_combinations)

    print("Keywords" + str(keywords))
    print("Total possible combinations found: " + str(len(final_combinations)))


    compare_guesses(final_combinations, password)




def create_password_strength_check(password):
    """Check if a password meets modern strength criteria."""
    if len(password) < 8:
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def sign_in_or_create_account(accounts):
    """Handle user sign-in or account creation."""
    choice = 0
    while choice != "3":
        choice = input("-----Welcome to FakeBook!-----\n\n1. Sign in\n2. Create New Account\n3. Exit\n")
        if choice == "1":
            user_id = input("Enter your user ID: ")
            password = input("Enter your password: ")
            if user_id in accounts and accounts[user_id] == password:
                print("Successfully signed in.")
                return user_id
            else:
                print("Incorrect user ID or password.")
        elif choice == "2":
            user_id = input("Choose your user ID: ")
            if user_id in accounts:
                print("This user ID is already taken.")
                continue
            password = input("Create your password: ")
            if not create_password_strength_check(password):
                print("Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.")
                continue
            accounts[user_id] = password
            save_json(accounts, accounts_file_path)
            print("Account created successfully. Please sign in.")
        elif choice != "3":
            print("Invalid choice. Please choose 'sign in' or 'create'.")
    return False

def user_menu(user_id):
    """Display menu for signed-in users."""
    while True:
        print("\nUser Menu:")
        print("1. View Posts")
        print("2. Make Post")
        print("3. Check Password Strength")
        print("4. Change Password")
        print("5. Sign Out")
        choice = input("Enter your choice (1-5): ")

        accounts = load_json(accounts_file_path)
        posts = load_json(posts_file_path)
        if choice == "1":
            view_posts(posts, user_id)
        elif choice == "2":
            make_post(posts, user_id)
        elif choice == "3":
            # password = input("Enter a password to check its strength: ")
            if constant_password_strength_check(user_id, posts, accounts[user_id]):
                print("This is a strong password.")
            else:
                print("This password is not strong enough.")
        elif choice == "4":
            change_password(user_id, accounts)
        elif choice == "5":
            print("Signing out...")
            break
        else:
            print("Invalid choice. Please select an option between 1 and 5.")

def change_password(user_id, accounts):
    """Allow a user to change their password."""
    new_password = input("Enter your new password: ")
    if not create_password_strength_check(new_password):
        print("Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.")
        return
    accounts[user_id] = new_password
    save_json(accounts, accounts_file_path)
    print("Password changed successfully.")


def view_posts(posts, user_id):
    """Displays all the posts related to the current signed in account"""
    posts = posts["users"]
    if not posts or user_id not in posts or not posts[user_id]['posts']:
        print("No posts available.")
        return
    for post in posts[user_id]['posts']:
        print(f"\nPost ID: {post['id']}\nContent: {post['content']}\nTimestamp: {post['timestamp']}\nLikes: {post['likes']}")
        for comment in post['comments']:
            print(f"Comment by {comment['author']}: {comment['comment']} on {comment['timestamp']}")

def make_post(posts, user_id):
    
    """Makes a post to the current signed in account and addds it to teh database"""
    content = input("Enter your post content: ")

    # Check if any word in the content is also in teh users password
    password = accounts.get(user_id)
    if password:
        if any(word.lower() in password.lower() for word in content.split()):
            response = input("Warning: Your post contains a word that is also in your password. Are you sure you want to proceed? (yes/no): ")
            if response.lower() != 'yes':
                print("Post creation canceled.")
                return

    new_post_id = posts["total_info"]["total_posts"] + 1
    new_post = {
        "id": new_post_id,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "likes": 0,
        "comments": []
    }
    # Check if user exists in posts["users"], if not, initialize their posts list
    if user_id not in posts["users"]:
        posts["users"][user_id] = {"posts": []}
    # Append the new post to the user's posts
    posts["users"][user_id]["posts"].append(new_post)
    # Update the total posts count
    posts["total_info"]["total_posts"] = new_post_id
    # Save changes
    save_json(posts, posts_file_path)
    print("Post added successfully.")


if __name__ == "__main__":
    accounts = load_json(accounts_file_path)
    posts = load_json(posts_file_path)

    user_id = sign_in_or_create_account(accounts)
    if user_id != False:
        print(user_id)
        user_menu(user_id)
