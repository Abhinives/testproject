import requests

def get_joke():
    """Fetches a random joke from the Official Joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke_data = response.json()
        print(f"Setup: {joke_data['setup']}")
        print(f"Punchline: {joke_data['punchline']}")
    except requests.RequestException as e:
        print(f"Failed to fetch a joke: {e}")

def main():
    print("Welcome to the Random Joke Generator!\n")
    get_joke()

if __name__ == "__main__":
    main()
