import sys
import io

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from chatbot import Chatbot

def main():
    bot = Chatbot()
    print("=" * 60)
    print("BUDDYBOT - YOUR FRIENDLY & MOTIVATING AI COMPANION")
    print("=" * 60)
    print("Share your feelings, ask for a joke, or get motivated!")
    print("Type 'bye', 'exit', or 'quit' to end the chat.")
    print("-" * 60)
    print("Bot: Hey there! How are you feeling today? I'm all ears! 😊")
    print("-" * 60)

    exit_commands = {"bye", "goodbye", "exit", "quit"}

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! Have a wonderful day!")
            break

        if not user_input:
            continue

        if user_input.lower() in exit_commands:
            print("Bot: Goodbye! Have a great day!")
            break

        reply = bot.respond(user_input)
        print(f"Bot: {reply}\n")

if __name__ == "__main__":
    main()
