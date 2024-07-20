import re
import random

class ChatBot:
    # Negative responses
    negative_responses = ("no", "not", "sorry", "not a chance", "bad")
    # Exit commands
    exit_commands = ("exit", "quit", "goodbye", "bye", "leave")

    def __init__(self):
        self.chat_responses = {
            'ask_about_service': r'.*\s*service.*',
            'technical_support': r'.*technical.*support.*',
            'about_returns': r'.*\s*returnpolicy.*',
            'general_query': r'.*how.*help.*'
        }

    def greet(self):
        self.name = input("Hello! What can I help you?\n")
        will_help = input(f"Hi {self.name}, how can I help you today?\n")
        if will_help.lower() in self.negative_responses:
            print("Alright, have a great day!")
        else:
            self.chat()

    def make_exit(self, reply):
        for command in self.exit_commands:
            if command in reply:
                print("Thanks for chatting with us. Have a great day!")
                return True
        return False

    def chat(self):
        reply = input("Please tell me your question: ").lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))

    def match_reply(self, reply):
        for intent, regex_pattern in self.chat_responses.items():
            found_match = re.search(regex_pattern, reply)
            if found_match and intent == 'ask_about_service':
                return self.ask_about_service()
            elif found_match and intent == 'technical_support':
                return self.technical_support()
            elif found_match and intent == 'about_returns':
                return self.about_returns()
            elif found_match and intent == 'general_query':
                return self.general_query()
        return self.no_match_intent()

    def ask_about_service(self):
        responses = ["Our service is top-one with excellent customer support!\n",
                     "You can find all the details about our services on our main website.\n"]
        return random.choice(responses)

    def technical_support(self):
        responses = ["You can visit our technical support at any time; it's available 24/7.\n",
                     "You can also call our technical support team anytime at our toll-free number: 1800182623.\n"]
        return random.choice(responses)

    def about_returns(self):
        responses = ["Our return policy allows returns within 30 days.\n",
                     "We provide service charge-free returns for our customers.\n"]
        return random.choice(responses)

    def general_query(self):
        responses = ["Feel free to ask any type of query about our service.\n",
                     "How can I assist you with this query?\n",
                     "Is there anything I can help you with today?\n",
                     "We provide the best quality services for our customers.\n",
                     "Feel free to ask any problems regarding our services in the query section.\n"]
        return random.choice(responses)

    def no_match_intent(self):
        responses = ["I'm sorry, I couldn't understand your problem.\n",
                     "Could you please elaborate on your query regarding the problem?\n"]
        return random.choice(responses)


bot = ChatBot()
bot.greet()
