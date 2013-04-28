import os
import csv

PATH = '/Users/kent/avec2013/final_features/'
TRAINING_LABEL_PATH = '/Users/kent/avec2013/Training_DepressionLabels/'
DEVELOPMENT_LABEL_PATH = '/Users/kent/avec2013/Development_DepressionLabels/'

# training
train_labels = [f for f in os.listdir(TRAINING_LABEL_PATH) if '.csv' in f]
with open(PATH+'avec_train.test','wb') as fw:
	writer = csv.writer(fw)
	for l in train_labels:
		with open(TRAINING_LABEL_PATH+l) as f:
			reader = csv.reader(f)
			label = [l for l in reader][0]
			binary_l = [0] if int(label[0])<=13 else [1]
			writer.writerow(binary_l)

# development
dev_labels = [f for f in os.listdir(DEVELOPMENT_LABEL_PATH) if '.csv' in f]
with open(PATH+'avec_dev.test','wb') as fw:
	writer = csv.writer(fw)
	for l in dev_labels:
		with open(DEVELOPMENT_LABEL_PATH+l) as f:
			reader = csv.reader(f)
			label = [l for l in reader][0]
			binary_l = [0] if int(label[0]) <=13 else [1]
			writer.writerow(binary_l)

