import re
import matplotlib.pyplot as plt
import numpy as np
import math

file = open("textMsgs.data.txt", "r")

contents = file.read()
filtered_words = ["the", "an", "a"]

#NEED TO CREATE A TRAINING(What it learns from) AND TEST(What it checks against) SAMPLE FROM THESE
breakup_of_messages = re.split(r"\n", contents)
breakup_of_messages.pop() #Removed empty split at end
print(len(breakup_of_messages))

vocab = []

class_counts = {"ham": 0, "spam": 0}
class_word_counts = {"ham": {}, "spam": {}}
class_total_word_counts = {"ham": 0, "spam": 0 }

training = []
testing = []

#Pull together a dictionary of vocab words
#Split into a training and test set by 2:1 ratio.
for i in range(0, len(breakup_of_messages)):
	if i%4 == 3:
		testing.append(breakup_of_messages[i])
	else:
		training.append(breakup_of_messages[i])

class_total_word_counts = {"ham": 0, "spam": 0 }
print("------")
for message in training:
	message = message.split()
	classification = message.pop(0)
	#print(classification)
	class_counts[classification] += 1
	for word in message:
		if word not in filtered_words:
			class_total_word_counts[classification] += 1
			if word not in vocab:
				vocab.append(word)
			if word not in class_word_counts[classification]:
				class_word_counts[classification][word] = 1
			else:
				class_word_counts[classification][word] += 1
print(class_total_word_counts["ham"])
print(class_total_word_counts["spam"])

train_size = len(training)
class_probability = {"ham": class_counts["ham"]/train_size, "spam": class_counts["spam"]/train_size}


TP = 0
FP = 0
FN = 0
TN = 0
for message in testing:
	message = message.split()
	classification = message.pop(0)

	ham_prob = class_counts["ham"]/(class_counts["ham"]+class_counts["spam"])
	spam_prob = class_counts["spam"]/(class_counts["ham"]+class_counts["spam"])

	for word in message:
		total_count = class_total_word_counts["ham"]+len(vocab)
		if word not in class_word_counts["ham"]:
			ham_prob += math.log(1/total_count)
		else:
			ham_prob += math.log((class_word_counts["ham"][word] + 1)/total_count)
		if word not in class_word_counts["spam"]:
			spam_prob += math.log(1/total_count)
		else:
			spam_prob += math.log((class_word_counts["spam"][word] + 1)/total_count)

	if (spam_prob > ham_prob):
		if classification == "spam":
			TN += 1
		else:
			FN += 1
	else:
		if classification == "ham":
			TP += 1
		else:
			print(ham_prob)
			print(spam_prob)
			print("______")
			FP += 1

print(TP)
print(FP)
print(FN)
print(TN)


