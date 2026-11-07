# BuddyBot

BuddyBot is a locally run, emotion-aware chatbot built with Python, Flask, NLTK, and scikit-learn. It combines rule-based responses with TF-IDF and cosine similarity to respond to everyday conversation, stress, sadness, and other emotions.

## Features

- Responsive browser-based chat interface
- Flask JSON chat endpoint
- Command-line mode
- Local corpus of conversational responses
- Downloads required NLTK data the first time it runs

## Run locally

1. Install Python 3.10 or later.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the web app:

   ```powershell
   python app.py
   ```

5. Open <http://127.0.0.1:5000> in your browser.

To use the command-line interface instead, run `python cli.py`.

The app runs locally by default. It is an educational project and is not a substitute for professional mental-health care.

## Documentation

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for the project overview, architecture, and technical details.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for the license text and attribution.
