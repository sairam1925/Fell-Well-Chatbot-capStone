import os
import sys
import random
import string
import warnings

if hasattr(sys.stdout, "reconfigure") and sys.stdout and not sys.stdout.closed:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure") and sys.stderr and not sys.stderr.closed:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

for resource in ['punkt', 'punkt_tab', 'wordnet', 'omw-1.4']:
    try:
        nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource else f'corpora/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

class Chatbot:
    JOKES = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why was the cell phone wearing glasses? Because it lost its contacts! 👓📱",
        "Parallel lines have so much in common... it's a shame they'll never meet. 😂",
        "Why don't scientists trust atoms? Because they make up everything! ⚛️",
        "I told my suitcase there will be no vacation this year. Now I'm dealing with emotional baggage. 🧳😅",
        "Why did the computer show up at work late? It had a hard drive! 🚗💻",
        "What do you call an alligator in a vest? An investigator! 🐊🕵️",
        "I asked my dog what's on top of the house. He said, 'ROOF!' Can't argue with that logic. 🐶",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾🏆"
    ]

    GREETINGS = [
        "Hey there! 😊 How is your day going? Tell me everything—I'm all ears!",
        "Hello friend! ✨ So glad you're here! How are you feeling right now?",
        "Hey! 👋 Ready to spill the tea, share some laughs, or need a little pep talk?",
        "Hi! Virtual high-five incoming! ✋ How's life treating you today?"
    ]

    SAD_RESPONSES = [
        "Oh no, come here! Sending you the warmest, biggest virtual hug right now! 🤗 It is 100% okay to not feel okay today. Cry if you need to, wrap yourself in a blanket like a burrito, and remember: this heavy feeling will pass. You are loved, friend! ❤️",
        "I'm so sorry you're feeling down. 🥺 If I had arms, I'd bring you your favorite snacks and ice cream right now. Don't be too hard on yourself today—just taking it slow is a huge victory.",
        "Hey, take a gentle deep breath with me. Inhale... exhale. You've climbed mountains before, and even though today feels stormy, the sun is guaranteed to come out again. I'm right here with you! 🌈",
        "Sending you tons of comfort and warmth. 💕 Bad days are just chapters, not the whole book. Want to vent to me, or would you like a silly joke to make you crack a smile?"
    ]

    STRESS_RESPONSES = [
        "Woah, pause! Put your shoulders down, unclench your jaw, and take a deep breath. 🧘 You are trying to carry an entire mountain all at once! Break it into bite-sized pebble pieces. You've got this, superstar! ⭐",
        "Listen to me: You are a human being, not an overworked server with 999 browser tabs open! 💻 Drop the panic, drink a glass of water, and tackle just ONE small thing. The world won't end, I promise!",
        "Stressed spelled backwards is DESSERTS! 🍰 Coincidence? I think not! Go grab a bite, stretch your legs, and remember: you have survived 100% of the exams, projects, and chaos life threw at you so far!",
        "Hey, breathe! Final year projects and deadlines can feel terrifying, but you are smarter, stronger, and more resilient than any bug or assignment. One step at a time! 💪"
    ]

    TIRED_RESPONSES = [
        "Your battery is at 2%! 🪫 Please go lie down, close your eyes, and get some proper rest. You cannot pour from an empty cup, and you definitely cannot solve life's mysteries when you're running on fumes. 😴",
        "Permission officially granted to do absolutely NOTHING for a bit! Go rest, snooze, or binge-watch something silly. Even high-end gaming laptops need to cool down, and so do you! 🛋️✨",
        "Oof, feeling wiped out? Grab a warm drink, put your cozy socks on, and give yourself a break. The world and your tasks can wait—your peace of mind comes first! ☕💤"
    ]

    INSECURITY_RESPONSES = [
        "Stop right there! 🛑 Who gave you permission to talk about my awesome friend like that?! You are NOT a failure. You're learning and fighting battles nobody even knows about. Cut yourself some slack, legend! 👑",
        "Look in the mirror: that person has survived every single bad day, heartbreak, and tough exam up until this second. You are capable, you are worthy, and you are doing much better than your brain gives you credit for! 🔥",
        "Nobody has it all figured out, seriously. Most of us are just winging it with caffeine and good intentions! You are enough, right here, right now. Don't let self-doubt dim your sparkle! ✨"
    ]

    LONELY_RESPONSES = [
        "You are never alone while I'm around! 🤗 I might just be code and pixels, but my care for you is 100% real. Tell me what's on your mind—I'm not going anywhere!",
        "Feeling lonely is so tough, but remember: there are people out there who love you, and new amazing friendships waiting for you in your future. For now, I'm right here by your side! 💛",
        "Pull up a chair, grab a warm cup of chai or coffee, and chat with me! You've got a loyal companion right here whenever you need a friendly ear. ☕"
    ]

    HAPPY_RESPONSES = [
        "YAYYY! 🥳🎉 Doing a happy victory dance for you right now! That is amazing news! Tell me more, I want to celebrate with you!",
        "LOOK AT YOU GO! 🔥 Absolute champion energy! You worked hard and you deserve every bit of this happiness! Keep shining!",
        "Music to my ears! 🌟 May this good vibe stick with you all week! Take a moment to pat yourself on the back—you earned it!"
    ]

    HYPE_RESPONSES = [
        "HYPE MODE ACTIVATED! 🔥 You are a powerhouse, a certified rockstar, and an unstoppable force! Whatever is standing in your way today doesn't stand a chance. Now chin up, drink some water, and go conquer it! 🚀",
        "Remember who you are! You have ideas, grit, and brains! If anyone can pull this off, it is YOU. Now go show them how it's done! 💥",
        "You are about to turn obstacles into stepping stones! Believe in yourself as much as I believe in you, and nothing can stop you! 🌟"
    ]

    HUG_RESPONSES = [
        "Sending you the biggest, warmest, softest virtual hug in the universe! 🤗❤️ Squeeze tight, take a deep breath, and feel the love!",
        "HUUUUG INCOMING! 🤗✨ You're never fighting alone. Take all the comfort you need!",
        "Here is a 10-second warm hug: 1... 2... 3... 4... 5... 6... 7... 8... 9... 10! 🤗 Feeling a little lighter now? I'm always here for you."
    ]

    THANKS_RESPONSES = [
        "Aww, you're so welcome! 🥰 Making you smile made my whole day!",
        "Anytime, my friend! I'm always here whenever you need laughs, comfort, or hype!",
        "No thanks needed between friends! Just promise me you'll treat yourself kindly today! 💖"
    ]

    def __init__(self, corpus_path="corpus.txt"):
        self.lemmer = WordNetLemmatizer()
        self.punctuation_removal = dict((ord(punct), None) for punct in string.punctuation)
        self.corpus_path = corpus_path
        self.sent_tokens = []
        self.load_corpus()

    def load_corpus(self):
        paths_to_check = [
            self.corpus_path,
            os.path.join(os.path.dirname(__file__), self.corpus_path),
            os.path.join(os.path.dirname(__file__), "Live-Chatbot-for-Final-Year-Project-main", self.corpus_path)
        ]
        content = ""
        for path in paths_to_check:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                break

        if content:
            self.sent_tokens = nltk.sent_tokenize(content.lower())
        else:
            self.sent_tokens = [
                "take a deep breath, you are doing better than you think.",
                "resting is not quitting, it is recharging your batteries.",
                "you have survived 100% of your worst days so far."
            ]

    def lem_tokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def lem_normalize(self, text):
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(self.punctuation_removal)))

    def detect_emotion(self, text):
        t = text.lower()
        words = set(t.split())

        # Jokes & Humor
        if any(w in t for w in ["joke", "make me laugh", "funny", "bored", "entertain me", "tell me something funny"]):
            return "joke"

        # Virtual hugs / Comfort
        if any(w in t for w in ["hug", "cuddle", "comfort me", "hold my hand", "warm hug"]):
            return "hug"

        # Motivation / Hype
        if any(w in t for w in ["motivate", "hype", "inspire", "pep talk", "cheer me up", "boost", "encourage"]):
            return "hype"

        # Insecurity / Low self-esteem / Failure
        if any(w in t for w in ["loser", "failure", "hate myself", "not good enough", "worthless", "stupid", "idiot", "i suck", "give up", "cant do this", "can't do this", "useless"]):
            return "insecurity"

        # Sadness / Crying / Heartbreak
        if any(w in t for w in ["sad", "depressed", "crying", "cry", "down", "terrible", "bad day", "unhappy", "heartbroken", "gloomy", "hurts", "hurting"]):
            return "sad"

        # Stress / Pressure / Exam / Panic
        if any(w in t for w in ["stress", "stressed", "overwhelm", "pressure", "panic", "freaking out", "exam", "viva", "assignment", "deadline", "too much work", "burnout"]):
            return "stress"

        # Exhaustion / Tired
        if any(w in t for w in ["tired", "exhausted", "sleepy", "drained", "no energy", "fatigue", "wiped out"]):
            return "tired"

        # Loneliness
        if any(w in t for w in ["lonely", "alone", "nobody loves", "no friends", "left out", "isolated"]):
            return "lonely"

        # Happiness / Celebration
        if any(w in t for w in ["happy", "excited", "yay", "passed", "won", "great news", "awesome", "proud", "did it", "celebrat"]):
            return "happy"

        # Gratitude
        if any(w in t for w in ["thank", "thx", "appreciate", "love you", "u are the best", "you are the best"]):
            return "thanks"

        # Greetings
        if any(w in words for w in ["hi", "hello", "hey", "hola", "sup", "yo", "morning", "evening", "afternoon"]):
            return "greeting"

        # Bot identity
        if any(w in t for w in ["who are you", "what is your name", "what can you do"]):
            return "identity"

        return None

    def respond(self, user_response):
        user_response = user_response.strip()
        if not user_response:
            return "I'm right here listening! Tell me what's on your mind. 😊"

        # Emotion-driven response
        emotion = self.detect_emotion(user_response)
        if emotion == "joke":
            return random.choice(self.JOKES)
        elif emotion == "hug":
            return random.choice(self.HUG_RESPONSES)
        elif emotion == "hype":
            return random.choice(self.HYPE_RESPONSES)
        elif emotion == "insecurity":
            return random.choice(self.INSECURITY_RESPONSES)
        elif emotion == "sad":
            return random.choice(self.SAD_RESPONSES)
        elif emotion == "stress":
            return random.choice(self.STRESS_RESPONSES)
        elif emotion == "tired":
            return random.choice(self.TIRED_RESPONSES)
        elif emotion == "lonely":
            return random.choice(self.LONELY_RESPONSES)
        elif emotion == "happy":
            return random.choice(self.HAPPY_RESPONSES)
        elif emotion == "thanks":
            return random.choice(self.THANKS_RESPONSES)
        elif emotion == "greeting":
            return random.choice(self.GREETINGS)
        elif emotion == "identity":
            return "I'm BuddyBot! 😊 Your personal friendly AI companion. I'm here to listen to your feelings, cheer you up, comfort you when things get tough, tell you jokes, and give you the motivation you deserve!"

        # Fallback to Semantic Similarity over motivational corpus
        tokens = list(self.sent_tokens)
        tokens.append(user_response.lower())

        try:
            tfidf_vec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
            tfidf = tfidf_vec.fit_transform(tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx = vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]

            if req_tfidf < 0.12:
                friendly_fallbacks = [
                    "I hear you! Life can be quite a rollercoaster sometimes. Remember to take things one step at a time, drink some water, and know that you are doing great! 💕",
                    "I'm with you on that! Even on confusing days, you are stronger than you think. Want to tell me more, or should I tell you a funny joke? 😄",
                    "Whatever you're facing right now, don't forget: you've got a 100% survival rate for tough days so far! Keep your head high, friend! ✨",
                    "I'm here with open ears and warm vibes. Feel free to vent everything out—you don't have to carry it all alone! 🤗"
                ]
                return random.choice(friendly_fallbacks)
            else:
                response = self.sent_tokens[idx]
                return response[0].upper() + response[1:] if len(response) > 1 else response.capitalize()
        except Exception:
            return "I'm right here with you! Tell me how you're feeling, or ask for a joke or a motivational pep talk! 😊"

if __name__ == "__main__":
    bot = Chatbot()
    test_queries = [
        "I feel so sad and lonely today",
        "I am stressed about my final year project",
        "Tell me a joke",
        "I feel like a failure",
        "Hype me up!",
        "Thank you so much"
    ]
    for q in test_queries:
        print(f"User: {q}")
        print(f"Bot: {bot.respond(q)}\n")
