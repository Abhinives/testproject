import requests
import random
import string

def get_joke():
    """Fetches a random joke from the Official Joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke_data = response.json()
        print("\n--- Joke ---")
        print(f"Setup: {joke_data['setup']}")
        print(f"Punchline: {joke_data['punchline']}")
        print("------------\n")
    except requests.RequestException as e:
        print(f"\n[Error] Failed to fetch a joke: {e}\n")

def get_trivia():
    """Fetches a random trivia question from the Open Trivia Database."""
    url = "https://opentdb.com/api.php?amount=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        trivia_data = response.json()
        if trivia_data['results']:
            question = trivia_data['results'][0]['question']
            answer = trivia_data['results'][0]['correct_answer']
            
            # Using basic HTML decoding for simple entities
            import html
            question = html.unescape(question)
            answer = html.unescape(answer)
            
            print("\n--- Trivia ---")
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print("--------------\n")
        else:
            print("\n[Error] No trivia found.\n")
    except requests.RequestException as e:
        print(f"\n[Error] Failed to fetch trivia: {e}\n")

def generate_password(length=12):
    """Generates a random password of given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    print("\n--- Password Generator ---")
    print(f"Your random password is: {password}")
    print("--------------------------\n")

def main():
    print("Welcome to the Multi-Tool Utility!")
    while True:
        print("Please choose an option:")
        print("1. Get a random joke")
        print("2. Get a random trivia question")
        print("3. Generate a random password")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            get_joke()
        elif choice == '2':
            get_trivia()
        elif choice == '3':
            generate_password()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("\n[Error] Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
