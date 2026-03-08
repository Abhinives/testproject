import requests
import random
import string
import math
import os
import json
import datetime


# ─────────────────────────────────────────────
# ORIGINAL FUNCTIONS (unchanged)
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# NEW FUNCTIONS
# ─────────────────────────────────────────────

# ── 1. Unit Converter ──────────────────────────────────────────────────────────

UNIT_CONVERSIONS = {
    "km_to_miles": 0.621371,
    "miles_to_km": 1.60934,
    "kg_to_lbs": 2.20462,
    "lbs_to_kg": 0.453592,
    "celsius_to_fahrenheit": None,   # handled specially
    "fahrenheit_to_celsius": None,   # handled specially
    "liters_to_gallons": 0.264172,
    "gallons_to_liters": 3.78541,
    "meters_to_feet": 3.28084,
    "feet_to_meters": 0.3048,
}

def convert_units(value, conversion_type):
    """
    Converts a value based on the specified conversion type.

    Supported types:
        km_to_miles, miles_to_km, kg_to_lbs, lbs_to_kg,
        celsius_to_fahrenheit, fahrenheit_to_celsius,
        liters_to_gallons, gallons_to_liters,
        meters_to_feet, feet_to_meters

    Args:
        value (float): The numeric value to convert.
        conversion_type (str): One of the supported conversion keys.

    Returns:
        float: The converted value, or None if the type is unsupported.
    """
    if conversion_type == "celsius_to_fahrenheit":
        return (value * 9 / 5) + 32
    elif conversion_type == "fahrenheit_to_celsius":
        return (value - 32) * 5 / 9
    elif conversion_type in UNIT_CONVERSIONS:
        factor = UNIT_CONVERSIONS[conversion_type]
        if factor is not None:
            return value * factor
    return None


def unit_converter_menu():
    """Interactive menu for the unit converter."""
    print("\n--- Unit Converter ---")
    print("Available conversions:")
    for i, key in enumerate(UNIT_CONVERSIONS.keys(), start=1):
        print(f"  {i}. {key.replace('_', ' ')}")

    conversion_keys = list(UNIT_CONVERSIONS.keys())
    try:
        choice = int(input("Select conversion (number): ")) - 1
        if choice < 0 or choice >= len(conversion_keys):
            print("[Error] Invalid selection.\n")
            return
        conversion_type = conversion_keys[choice]
        value = float(input("Enter value to convert: "))
        result = convert_units(value, conversion_type)
        if result is not None:
            print(f"Result: {value} → {result:.4f}  ({conversion_type.replace('_', ' ')})")
        else:
            print("[Error] Conversion not supported.")
    except ValueError:
        print("[Error] Please enter a valid number.")
    print("----------------------\n")


# ── 2. Simple Calculator ───────────────────────────────────────────────────────

def calculator():
    """
    A simple command-line calculator supporting +, -, *, /, **, and %.
    
    BUG #1 (intentional): Division does NOT guard against zero division —
    the except clause catches the ZeroDivisionError but re-raises it instead
    of printing a friendly message, so the program will crash.
    """
    print("\n--- Calculator ---")
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /, **, %): ").strip()
        b = float(input("Enter second number: "))

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            # BUG: raises ZeroDivisionError instead of handling gracefully
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result = a / b
        elif op == "**":
            result = a ** b
        elif op == "%":
            result = a % b
        else:
            print("[Error] Unsupported operator.")
            return

        print(f"Result: {a} {op} {b} = {result}")
    except ZeroDivisionError as e:
        raise   # BUG: should print error message, not re-raise and crash
    except ValueError:
        print("[Error] Invalid number entered.")
    print("------------------\n")


# ── 3. Number Guessing Game ────────────────────────────────────────────────────

def number_guessing_game():
    """
    A simple number guessing game.
    The computer picks a random integer between 1 and 100 (inclusive).
    The player has up to 7 attempts to guess correctly.
    After each wrong guess the program hints 'Too high' or 'Too low'.
    """
    print("\n--- Number Guessing Game ---")
    secret = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("I've picked a number between 1 and 100. You have 7 attempts.")

    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} — Your guess: "))
        except ValueError:
            print("  Please enter a whole number.")
            continue

        attempts += 1

        if guess == secret:
            print(f"  🎉 Correct! You guessed it in {attempts} attempt(s).")
            break
        elif guess < secret:
            print("  Too low!")
        else:
            print("  Too high!")
    else:
        print(f"  Game over! The number was {secret}.")

    print("----------------------------\n")


# ── 4. To-Do List Manager ──────────────────────────────────────────────────────

class TodoManager:
    """
    In-memory to-do list manager.

    Supports adding, completing, deleting, and listing tasks.
    Tasks are stored as dicts with keys: id, title, done, created_at.
    """

    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def add_task(self, title: str) -> dict:
        """Add a new task and return it."""
        task = {
            "id": self._next_id,
            "title": title.strip(),
            "done": False,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self._tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as done. Returns True on success, False if not found."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["done"] = True
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by id. Returns True on success, False if not found."""
        for i, task in enumerate(self._tasks):
            if task["id"] == task_id:
                self._tasks.pop(i)
                return True
        return False

    def list_tasks(self, show_done: bool = True) -> list:
        """Return tasks, optionally filtering out completed ones."""
        if show_done:
            return list(self._tasks)
        return [t for t in self._tasks if not t["done"]]

    def __len__(self):
        return len(self._tasks)


_todo = TodoManager()


def todo_menu():
    """Interactive to-do list menu."""
    print("\n--- To-Do List ---")
    while True:
        print("\n  1. Add task")
        print("  2. Complete task")
        print("  3. Delete task")
        print("  4. List all tasks")
        print("  5. List pending tasks")
        print("  6. Back to main menu")

        choice = input("  Choice: ").strip()

        if choice == "1":
            title = input("  Task title: ").strip()
            if title:
                task = _todo.add_task(title)
                print(f"  Added task #{task['id']}: {task['title']}")
            else:
                print("  [Error] Title cannot be empty.")

        elif choice == "2":
            try:
                tid = int(input("  Task ID to complete: "))
                if _todo.complete_task(tid):
                    print(f"  Task #{tid} marked as done.")
                else:
                    print(f"  [Error] Task #{tid} not found.")
            except ValueError:
                print("  [Error] Enter a valid integer ID.")

        elif choice == "3":
            try:
                tid = int(input("  Task ID to delete: "))
                if _todo.delete_task(tid):
                    print(f"  Task #{tid} deleted.")
                else:
                    print(f"  [Error] Task #{tid} not found.")
            except ValueError:
                print("  [Error] Enter a valid integer ID.")

        elif choice == "4":
            tasks = _todo.list_tasks(show_done=True)
            if not tasks:
                print("  No tasks yet.")
            for t in tasks:
                status = "✓" if t["done"] else "○"
                print(f"  [{status}] #{t['id']} {t['title']}  ({t['created_at']})")

        elif choice == "5":
            tasks = _todo.list_tasks(show_done=False)
            if not tasks:
                print("  No pending tasks.")
            for t in tasks:
                print(f"  [○] #{t['id']} {t['title']}  ({t['created_at']})")

        elif choice == "6":
            break
        else:
            print("  [Error] Invalid choice.")

    print("------------------\n")


# ── 5. Basic Statistics Calculator ────────────────────────────────────────────

def compute_statistics(numbers: list) -> dict:
    """
    Compute basic descriptive statistics for a list of numbers.

    Returns a dict with: count, mean, median, mode, variance, std_dev,
    minimum, maximum, and range.

    Args:
        numbers (list of float/int): Input data. Must not be empty.

    Returns:
        dict: Statistics results.

    Raises:
        ValueError: If the input list is empty.
    """
    if not numbers:
        raise ValueError("Cannot compute statistics on an empty list.")

    n = len(numbers)
    total = sum(numbers)
    mean = total / n

    sorted_nums = sorted(numbers)
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]

    # Mode: most frequent value (first one if tie)
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    mode = max(freq, key=freq.get)

    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)

    return {
        "count": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": mode,
        "variance": round(variance, 4),
        "std_dev": round(std_dev, 4),
        "minimum": sorted_nums[0],
        "maximum": sorted_nums[-1],
        "range": sorted_nums[-1] - sorted_nums[0],
    }


def statistics_menu():
    """Interactive statistics calculator."""
    print("\n--- Statistics Calculator ---")
    raw = input("Enter numbers separated by spaces: ").strip()
    try:
        numbers = [float(x) for x in raw.split()]
        if not numbers:
            raise ValueError("No numbers provided.")
        stats = compute_statistics(numbers)
        print("\n  Results:")
        for key, val in stats.items():
            print(f"    {key:<12}: {val}")
    except ValueError as e:
        print(f"  [Error] {e}")
    print("-----------------------------\n")


# ── 6. Caesar Cipher ──────────────────────────────────────────────────────────

def caesar_cipher(text: str, shift: int, mode: str = "encrypt") -> str:
    """
    Encrypt or decrypt text using a Caesar cipher.

    Only alphabetic characters are shifted; all other characters are
    preserved as-is. Case is preserved.

    Args:
        text (str): The input text.
        shift (int): Number of positions to shift (0–25).
        mode (str): 'encrypt' or 'decrypt'.

    Returns:
        str: The transformed text.
    """
    if mode == "decrypt":
        shift = -shift

    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return "".join(result)


def caesar_cipher_menu():
    """Interactive Caesar cipher tool."""
    print("\n--- Caesar Cipher ---")
    text = input("Enter text: ")
    try:
        shift = int(input("Enter shift (0-25): "))
        if not 0 <= shift <= 25:
            print("[Error] Shift must be between 0 and 25.")
            return
    except ValueError:
        print("[Error] Shift must be an integer.")
        return

    mode = input("Encrypt or decrypt? (e/d): ").strip().lower()
    if mode not in ("e", "d"):
        print("[Error] Enter 'e' for encrypt or 'd' for decrypt.")
        return

    action = "encrypt" if mode == "e" else "decrypt"
    output = caesar_cipher(text, shift, mode=action)
    print(f"  Output: {output}")
    print("---------------------\n")


# ── 7. File Word-Frequency Counter ────────────────────────────────────────────

def word_frequency(text: str, top_n: int = 10) -> list:
    """
    Return the top_n most common words in a block of text.

    Words are normalised to lowercase, and non-alphanumeric characters
    (except apostrophes) are stripped from word boundaries.

    Args:
        text (str): Input text.
        top_n (int): Number of top words to return.

    Returns:
        list of (word, count) tuples sorted by frequency descending.
    """
    import re
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq[:top_n]


def word_frequency_menu():
    """Interactive word-frequency counter."""
    print("\n--- Word Frequency Counter ---")
    print("Options:")
    print("  1. Enter text manually")
    print("  2. Read from a file")
    choice = input("Choice: ").strip()

    if choice == "1":
        print("Enter/paste text (type END on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        text = "\n".join(lines)

    elif choice == "2":
        path = input("File path: ").strip()
        # BUG #2 (intentional): file is opened without specifying encoding,
        # which will fail on non-ASCII files on systems where the default
        # locale is not UTF-8 (e.g. Windows with cp1252). Should be:
        #   open(path, "r", encoding="utf-8")
        try:
            with open(path, "r") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"[Error] File not found: {path}")
            return
        except OSError as e:
            print(f"[Error] Could not read file: {e}")
            return
    else:
        print("[Error] Invalid choice.")
        return

    if not text.strip():
        print("[Error] No text to analyse.")
        return

    top_n_input = input("How many top words to show? (default 10): ").strip()
    top_n = int(top_n_input) if top_n_input.isdigit() else 10

    results = word_frequency(text, top_n=top_n)
    print(f"\n  Top {top_n} words:")
    for rank, (word, count) in enumerate(results, start=1):
        print(f"    {rank:>3}. {word:<20} {count}")
    print("------------------------------\n")


# ── 8. Fibonacci Generator ────────────────────────────────────────────────────

def fibonacci(n: int) -> list:
    """
    Return the first n Fibonacci numbers as a list.

    Args:
        n (int): How many Fibonacci numbers to generate. Must be >= 1.

    Returns:
        list of int: Fibonacci sequence starting from 0.

    Raises:
        ValueError: If n < 1.
    """
    if n < 1:
        raise ValueError("n must be at least 1.")
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def fibonacci_menu():
    """Interactive Fibonacci generator."""
    print("\n--- Fibonacci Generator ---")
    try:
        n = int(input("How many Fibonacci numbers? "))
        seq = fibonacci(n)
        print(f"  First {n} Fibonacci number(s): {seq}")
    except ValueError as e:
        print(f"  [Error] {e}")
    print("---------------------------\n")


# ── 9. Simple Contact Book ────────────────────────────────────────────────────

class ContactBook:
    """
    A simple in-memory contact book.

    Each contact has a name, phone, and optional email.
    Contacts are looked up by name (case-insensitive).
    """

    def __init__(self):
        self._contacts = {}   # name (lower) → dict

    def add_contact(self, name: str, phone: str, email: str = "") -> None:
        """Add or overwrite a contact."""
        key = name.strip().lower()
        self._contacts[key] = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }

    def find_contact(self, name: str) -> dict | None:
        """Return a contact dict or None if not found."""
        return self._contacts.get(name.strip().lower())

    def delete_contact(self, name: str) -> bool:
        """Delete a contact. Returns True if deleted, False if not found."""
        key = name.strip().lower()
        if key in self._contacts:
            del self._contacts[key]
            return True
        return False

    def all_contacts(self) -> list:
        """Return all contacts sorted alphabetically by name."""
        return sorted(self._contacts.values(), key=lambda c: c["name"].lower())

    def __len__(self):
        return len(self._contacts)


_contacts = ContactBook()


def contact_book_menu():
    """Interactive contact book menu."""
    print("\n--- Contact Book ---")
    while True:
        print("\n  1. Add contact")
        print("  2. Find contact")
        print("  3. Delete contact")
        print("  4. List all contacts")
        print("  5. Back to main menu")

        choice = input("  Choice: ").strip()

        if choice == "1":
            name = input("  Name: ").strip()
            phone = input("  Phone: ").strip()
            email = input("  Email (optional): ").strip()
            if name and phone:
                _contacts.add_contact(name, phone, email)
                print(f"  Contact '{name}' saved.")
            else:
                print("  [Error] Name and phone are required.")

        elif choice == "2":
            name = input("  Name to search: ").strip()
            contact = _contacts.find_contact(name)
            if contact:
                print(f"  Name : {contact['name']}")
                print(f"  Phone: {contact['phone']}")
                if contact["email"]:
                    print(f"  Email: {contact['email']}")
            else:
                print(f"  [Error] No contact found for '{name}'.")

        elif choice == "3":
            name = input("  Name to delete: ").strip()
            if _contacts.delete_contact(name):
                print(f"  Contact '{name}' deleted.")
            else:
                print(f"  [Error] No contact found for '{name}'.")

        elif choice == "4":
            all_c = _contacts.all_contacts()
            if not all_c:
                print("  Contact book is empty.")
            for c in all_c:
                line = f"  {c['name']}  |  {c['phone']}"
                if c["email"]:
                    line += f"  |  {c['email']}"
                print(line)

        elif choice == "5":
            break
        else:
            print("  [Error] Invalid choice.")

    print("--------------------\n")


# ── 10. Countdown Timer (non-blocking display) ────────────────────────────────

def countdown_timer():
    """
    A simple countdown timer.
    Counts down from a user-specified number of seconds,
    printing the remaining time every second.
    """
    import time
    print("\n--- Countdown Timer ---")
    try:
        seconds = int(input("Enter countdown duration in seconds: "))
        if seconds <= 0:
            print("[Error] Duration must be positive.")
            return
    except ValueError:
        print("[Error] Please enter a whole number.")
        return

    print(f"  Starting countdown from {seconds}s...")
    for remaining in range(seconds, 0, -1):
        print(f"  {remaining}s remaining...", end="\r")
        time.sleep(1)
    print("  ⏰ Time's up!                    ")
    print("-----------------------\n")


# ─────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────

def main():
    print("Welcome to the Multi-Tool Utility!")
    while True:
        print("Please choose an option:")
        print(" 1.  Get a random joke")
        print(" 2.  Get a random trivia question")
        print(" 3.  Generate a random password")
        print(" 4.  Unit converter")
        print(" 5.  Calculator")
        print(" 6.  Number guessing game")
        print(" 7.  To-do list manager")
        print(" 8.  Statistics calculator")
        print(" 9.  Caesar cipher")
        print(" 10. Word frequency counter")
        print(" 11. Fibonacci generator")
        print(" 12. Contact book")
        print(" 13. Countdown timer")
        print(" 14. Exit")

        choice = input("\nEnter your choice (1-14): ").strip()

        if choice == "1":
            get_joke()
        elif choice == "2":
            get_trivia()
        elif choice == "3":
            generate_password()
        elif choice == "4":
            unit_converter_menu()
        elif choice == "5":
            calculator()
        elif choice == "6":
            number_guessing_game()
        elif choice == "7":
            todo_menu()
        elif choice == "8":
            statistics_menu()
        elif choice == "9":
            caesar_cipher_menu()
        elif choice == "10":
            word_frequency_menu()
        elif choice == "11":
            fibonacci_menu()
        elif choice == "12":
            contact_book_menu()
        elif choice == "13":
            countdown_timer()
        elif choice == "14":
            print("Goodbye!")
            break
        else:
            print("\n[Error] Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()