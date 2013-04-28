import os
import csv

PATH = '/Users/kent/avec2013/final_features/'
TRAINING_DATA_PATH = '/Users/kent/avec2013/final_features/training/'
DEVELOPMENT_DATA_PATH = '/Users/kent/avec2013/final_features/development/'
TRAINING_LABEL_PATH = '/Users/kent/avec2013/Training_DepressionLabels/'
DEVELOPMENT_LABEL_PATH = '/Users/kent/avec2013/Development_DepressionLabels/'
TRAINING_BIN_PATH =  '/Users/kent/avec2013/final_features/train_bin/'
DEVELOPMENT_BIN_PATH =  '/Users/kent/avec2013/final_features/dev_bin/'

# training

train_data_files = [f for f in os.listdir(TRAINING_DATA_PATH) if '.csv' in f] 
train_labels = [f for f in os.listdir(TRAINING_LABEL_PATH) if '.csv' in f]

with open(PATH+'train_bin.csv','wb') as fw:
	writer = csv.writer(fw)
	for label_file in train_labels:
		label_id = label_file[:5]
		train_file = TRAINING_DATA_PATH +[x for x in train_data_files if x[:5]==label_id][0]
		with open(TRAINING_LABEL_PATH+label_file) as f:
			reader = csv.reader(f)
			label = [l for l in reader][0]
			with open(train_file) as fi:
				features = [x for x in csv.reader(fi)][0]
				features = label + features
				writer.writerow(features)

# development

dev_data_files = [f for f in os.listdir(DEVELOPMENT_DATA_PATH) if '.csv' in f]
dev_labels = [f for f in os.listdir(DEVELOPMENT_LABEL_PATH) if '.csv' in f]
with open(PATH+'dev_bin.csv','wb') as fw:
	writer = csv.writer(fw)
	for label_file in dev_labels:
		label_id = label_file[:5]
		dev_file = DEVELOPMENT_DATA_PATH+[x for x in dev_data_files if x[:5]==label_id][0]
		with open(DEVELOPMENT_LABEL_PATH+label_file) as f:
			reader = csv.reader(f)
			label = [l for l in reader][0]
			with open(dev_file) as fi:
				features = [x for x in csv.reader(fi)][0]
				features = label + features
				writer.writerow(features)

