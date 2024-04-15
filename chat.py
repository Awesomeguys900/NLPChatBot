from itertools import dropwhile
import random
import json
import torch
import datetime
import threading, re
import numpy as np
from model import NeuraNet
from nltk_utils import bag_of_words, tokenize
from ExtraFunctionality import get_current_time, set_timer, mathsSolver

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
with open("intents.json", "r") as file:
    intents = json.load(file)

FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuraNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# ------
botName = "AviBot"


def get_Response(sentence):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Softmax
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if tag == "time_check":
                    current_time = get_current_time()
                    response = random.choice(intent["responses"])
                    formattedResponse = response % current_time
                    return f"{botName}: {formattedResponse}"
                elif tag == "set_timer":
                    seconds = int(input(f"{botName}: How many seconds?\nYou: "))
                    set_timer(seconds, botName)
                elif tag == "math_help":
                    expression = input(
                        f"{botName}: {random.choice(intent['responses'])}\nYou: "
                    )
                    result = mathsSolver(expression)
                    return f"{botName}: Uhhh, is it: {result}. Lets hope so :D"
                else:
                    return f"{botName}: {random.choice(intent['responses'])}"
    else:
        return f"{botName}: I do not understand..."


# print("Lets chat! Type 'quit' to exit")
# while True:
#     sentence = input("You: ")
#     if sentence == "quit" or sentence == "exit":
#         break
#     sentence = tokenize(sentence)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)
#     output = model(X)
#     _, predicted = torch.max(output, dim=1)
#     tag = tags[predicted.item()]

#     # Softmax
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents["intents"]:
#             if tag == intent["tag"]:
#                 if tag == "time_check":
#                     current_time = get_current_time()
#                     response = random.choice(intent["responses"])
#                     formattedResponse = response % current_time
#                     print(f"{botName}: {formattedResponse}")
#                 elif tag == "set_timer":
#                     seconds = int(input(f"{botName}: How many seconds?\nYou: "))
#                     set_timer(seconds, botName)
#                 elif tag == "math_help":
#                     expression = input(
#                         f"{botName}: {random.choice(intent['responses'])}\nYou: "
#                     )
#                     result = mathsSolver(expression)
#                     print(f"{botName}: Uhhh, is it: {result}. Lets hope so :D")
#                 else:
#                     print(f"{botName}: {random.choice(intent['responses'])}")
#     else:
#         print(f"{botName}: I do not understand...")
