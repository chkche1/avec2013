import os
import csv
import sys
import copy

# Training 
MALE_TRAIN =['213_1','214_1','217_2','217_3','219_1','219_3','225_2','227_2','230_1','232_1','233_1','241_2','242_3','306_3','317_1','317_3','324_1','329_1']
FEMALE_TRAIN = ['203_1','205_2','207_2','208_2','209_1','215_2','215_3','223_1','223_2','226_1','228_1','229_2','234_3','236_1','237_3','238_2','239_1','240_1','240_2','243_1','308_3','310_4','312_2','318_2','318_3','320_1','320_2','321_2','322_1','331_1','332_2','332_4']

# Development
MALE_DEV =['204_1','206_1','213_2','213_3','214_2','219_2','221_1','225_1','227_1','232_2','241_1','241_3','242_2','244_1','306_2','313_3']

FEMALE_DEV =['205_1','207_1','208_1','209_2','211_1','215_1','216_1','216_2','218_1','218_2','220_2','222_1','228_2','229_1','231_1','234_1','236_2','237_2','238_3','239_2','239_3','310_1','310_3','316_2','318_1','319_1','320_3','321_1','323_1','323_3','326_1','331_3','332_1','333_1']

MALE = MALE_TRAIN + MALE_DEV
FEMALE = FEMALE_TRAIN + FEMALE_DEV

# Path

PATH = '/Users/kent/avec2013/New Data'
TEST_ORDER = '/Users/kent/avec2013/New Data/file_order.test' 
TRAIN_ORDER = '/Users/kent/avec2013/New Data/file_order.train'
TRAIN_FILE = '/Users/kent/avec2013/New Data/training/real11_scale.train'
TEST_FILE = '/Users/kent/avec2013/New Data/testing/real11_scale.test'

DEP_TRAIN_PATH = '/Users/kent/avec2013/New Data/training/dep_rank.train'
DEP_TEST_PATH = '/Users/kent/avec2013/New Data/testing/dep_rank.test'
NEU_TRAIN_PATH = '/Users/kent/avec2013/New Data/training/neu_rank.train'
NEU_TEST_PATH = '/Users/kent/avec2013/New Data/testing/neu_rank.test'

# Create easy lookup table
train_gender = []
test_gender = []
with open(TEST_ORDER,'rU') as f:
	for line in f:
		uid = os.path.basename(line)[:5]
		if uid in FEMALE:
			test_gender.append('1')
		else:
			test_gender.append('2')

with open(TRAIN_ORDER,'rU') as f:
	for line in f:
		uid = os.path.basename(line)[:5]
		if uid in FEMALE:
			train_gender.append('1')
		else:
			train_gender.append('2')	

female_query_train = []
male_query_train = []
neu_f_query_train = []
neu_m_query_train = []
with open(TRAIN_FILE, 'rU') as f:
	for  line_no, features in enumerate(f):
		gender = train_gender[line_no]
		fl = features.split()
		fl.insert(1,'qid='+gender)
		neu_fl = copy.deepcopy(fl)
		neu = '1' if int(fl[0])>13 else '0'
		neu_fl[0] = neu
		line = ' '.join(fl)
		nline = ' '.join(neu_fl)
		if gender == '1':
			female_query_train.append(line+'\n')
			neu_f_query_train.append(nline+'\n')
		else:
			male_query_train.append(line+'\n')
			neu_m_query_train.append(nline+'\n')

female_query_test = []
male_query_test = []
neu_f_query_test = []
neu_m_query_test = []
with open(TEST_FILE, 'rU') as f:
	for  line_no, features in enumerate(f):
		gender = test_gender[line_no]
		fl = features.split()
		fl.insert(1,'qid='+gender)
		neu_fl = copy.deepcopy(fl)
		neu = '1' if int(fl[0])>13 else '0'
		neu_fl[0] = neu
		line = ' '.join(fl)
		nline = ' '.join(neu_fl)
		if gender == '1':
			female_query_test.append(line+'\n')
			neu_f_query_test.append(nline+'\n')
		else:
			male_query_test.append(line+'\n')
			neu_m_query_test.append(nline+'\n')

# Convert to svm rank format

with open(DEP_TRAIN_PATH, 'w') as fw:
	fw.writelines(female_query_train)
	fw.writelines(male_query_train)

with open(DEP_TEST_PATH, 'w') as fw:
	fw.writelines(female_query_test)
	fw.writelines(male_query_test)

with open(NEU_TRAIN_PATH, 'w') as fw:
	fw.writelines(neu_f_query_train)
	fw.writelines(neu_m_query_train)

with open(NEU_TEST_PATH, 'w') as fw:
	fw.writelines(neu_f_query_test)
	fw.writelines(neu_m_query_test)


