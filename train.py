import json
import numpy as np
from nltk_utils import tokenize, stem, bag_of_words
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuraNet

with open("intents.json", "r") as file:
    intents = json.load(file)

all_words = []
tags = []
xy = []
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ["?", "!", ".", ","]
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []  # tag of the pattern
y_train = []

for pattern_sentence, tag in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)  # indexes of tags
    y_train.append(label)  # CrossEntropyLoss

X_train = np.array(X_train)
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # dataset[idx]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


# Hyperparameters
batchsize = 8
hidden_size = 8
output_size = len(tags)  # all tags/catageories
input_size = len(X_train[0])  # length of the bag of words
learningrate = 0.001  # how fast the model learns
numepochs = 1000  # number of iterations

dataset = ChatDataset()
train_loader = DataLoader(
    dataset=dataset, batch_size=batchsize, shuffle=True, num_workers=0
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuraNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learningrate)

for epoch in range(numepochs):
    for words, labels in train_loader:
        words = words.to(device)
        labels = labels.to(device)
        # Forward pass
        # inputs are the bag of words
        outputs = model(words)
        loss = criterion(outputs, labels)
        # Backward and optimize step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"epoch {epoch+1}/{numepochs}, loss={loss.item():.4f}")

print(f"final loss, loss={loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags,
}

FILE = "data.pth"
torch.save(data, FILE)
print(f"training complete. file saved to {FILE}")
