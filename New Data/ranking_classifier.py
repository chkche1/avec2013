import numpy
import os
from random import uniform, sample

DEP_PREDICT_PATH = '/Users/kent/avec2013/New Data/prediction/dep_rank.predict'
NEU_PREDICT_PATH = '/Users/kent/avec2013/New Data/prediction/neu_rank.predict'
PROB_PATH = '/Users/kent/avec2013/New Data/prediction/bin11_prob.test.predict'
TEST_ORDER = '/Users/kent/avec2013/New Data/file_order.test' 
ANS = '/Users/kent/avec2013/New Data/testing/bin11_scale.test'


from random import uniform, sample

def order(x, NoneIsLast = True, decreasing = False):
    """
    Returns the ordering of the elements of x. The list
    [ x[j] for j in order(x) ] is a sorted version of x.

    Missing values in x are indicated by None. If NoneIsLast is true,
    then missing values are ordered to be at the end.
    Otherwise, they are ordered at the beginning.
    """
    omitNone = False
    if NoneIsLast == None:
        NoneIsLast = True
        omitNone = True
        
    n  = len(x)
    ix = range(n)
    if None not in x:
        ix.sort(reverse = decreasing, key = lambda j : x[j])
    else:
        # Handle None values properly.
        def key(i, x = x):
            elem = x[i]
            # Valid values are True or False only.
            if decreasing == NoneIsLast:
                return not(elem is None), elem
            else:
                return elem is None, elem
        ix = range(n)
        ix.sort(key=key, reverse=decreasing)
            
    if omitNone:
        n = len(x)
        for i in range(n-1, -1, -1):
            if x[ix[i]] == None:
                n -= 1
        return ix[:n]
    return ix

def rank(x, NoneIsLast=True, decreasing = False, ties = "first"):
    """
    Returns the ranking of the elements of x. The position of the first
    element in the original vector is rank[0] in the sorted vector.

    Missing values are indicated by None.  Calls the order() function.
    Ties are NOT averaged by default. Choices are:
         "first" "average" "min" "max" "random" "average"
    """
    omitNone = False
    if NoneIsLast == None:
        NoneIsLast = True
        omitNone = True
    O = order(x, NoneIsLast = NoneIsLast, decreasing = decreasing)
    R = O[:]
    n = len(O)
    for i in range(n):
        R[O[i]] = i
    if ties == "first" or ties not in ["first", "average", "min", "max", "random"]:
        return R
        
    blocks     = []
    isnewblock = True
    newblock   = []
    for i in range(1,n) :
        if x[O[i]] == x[O[i-1]]:
            if i-1 not in newblock:
                newblock.append(i-1)
            newblock.append(i)
        else:
            if len(newblock) > 0:
                blocks.append(newblock)
                newblock = []
    if len(newblock) > 0:
        blocks.append(newblock)

    for i, block  in enumerate(blocks):
        # Don't process blocks of None values.
        if x[O[block[0]]] == None:
            continue
        if ties == "average":
            s = 0.0
            for j in block:
                s += j
            s /= float(len(block))
            for j in block:
                R[O[j]] = s                
        elif ties == "min":
            s = min(block)
            for j in block:
                R[O[j]] = s                
        elif ties == "max":
            s =max(block)
            for j in block:
                R[O[j]] = s                
        elif ties == "random":
            s = sample([O[i] for i in block], len(block))
            for i,j in enumerate(block):
                R[O[j]] = s[i]
        else:
            for i,j in enumerate(block):
                R[O[j]] = j
    if omitNone:
        R = [ R[j] for j in range(n) if x[j] != None]
    return R


ans = []
with open(ANS, 'rU') as f:
	for line in f:
		label = line.split()[0]
		label = 0 if label=='-1' else 1
		ans.append(label)

test_order = []
with open(TEST_ORDER,'rU') as f:
	for line in f:
		uid = os.path.basename(line)[:5]
		test_order.append(uid)



temp = []
with open(DEP_PREDICT_PATH, 'rU') as f:
	for line in f:
		temp.append(float(line))
ranks = rank(temp, decreasing=True)

d_scores = {}
for idx, t in enumerate(temp):
	r = 1-(ranks[idx]+1)/float(len(temp))
	d_scores[test_order[idx]] = r

temp = []
with open(NEU_PREDICT_PATH, 'rU') as f:
	for line in f:
		temp.append(float(line))
        ranks = rank(temp,decreasing=True)

n_scores ={}
for idx, t in enumerate(temp):
	r = 1-(ranks[idx]+1)/float(len(temp))
	n_scores[test_order[idx]] = r

prob = {}
with open(PROB_PATH, 'rU') as f:
	for idx, line in enumerate(f):
		if idx==0:
			continue
		label, prob_neu, prob_dep = line.split()
		prob[test_order[idx-1]] = (prob_neu,prob_dep)

print prob

# PRODUCT RULE

product_predict = []
mean_predict = []
max_predict = []

for t in test_order:
	pn, pd = prob[t]
	d_s = d_scores[t]
	n_s = d_scores[t]
	prob_n = float(pn)
	prob_d = float(pd)
	F_product = [prob_n*n_s, prob_d*d_s]
	F_mean = [(prob_n+n_s)/2, (prob_d+d_s)/2]
	F_max = [max(prob_n,n_s), max(prob_d,d_s)]

	product_predict.append(F_product.index(max(F_product)))
	mean_predict.append(F_mean.index(max(F_mean)))
	max_predict.append(F_max.index(max(F_max)))

print ans
print product_predict
print mean_predict
print max_predict

product_score, mean_score, max_score = 0,0,0
for idx, label in enumerate(ans):
	if product_predict[idx]==label:
		product_score +=1
	if mean_predict[idx] ==label:
		mean_score +=1
	if max_predict[idx] ==label:
		max_score += 1

N = len(ans)

print 'product: ',product_score/float(N)
print 'mean: ',mean_score/float(N)
print 'max: ',max_score/float(N)
