# Date: 2021/1/20
# Author: Qianqian Peng
#reference: Introduction to Algorithms
"""
近期利用pubannotation标注trait mention和gene，在这个过程中，用的最多的就是
re模块中的正则匹配，闲来无聊，就根据算法导论中字符串匹配章节对四种低阶到
高阶字符串匹配算法的描述，对伪代码进行进行python代码的实现。
包括：Naive string matching、Rabin-Karp string matching、
Finite automaton string matching、Knuth-Morris-Pratt string matching
"""

def naive_string_matcher(str1,str2,adjacent_character=None):
	'''
	:param str1: searching string
	:param str2: database string
	:return: the span list where str1 matchs sub-str2
	'''
	matching_result = []
	if not str1 or not str2:
		return matching_result
	if len(str1) > len(str2):
		return matching_result
	len1 = len(str1)
	len2 = len(str2)
	if adjacent_character is None:
		for i in range(len2-len1+1):
			if str2[i:i+len1] == str1:
				matching_result.append((i,i+len1))
		return matching_result
	else:
		if len1 == len2:
			if str1 == str2:
				matching_result.append((0,len2))
				return matching_result
		else:
			if str1 + adjacent_character == str2[0:len1+1]:
				matching_result.append((0,len1))
			str1_extend = adjacent_character + str1 + adjacent_character
			for i in range(1,len2-len1):
				if str1_extend == str2[i-1:i+len1+1]:
					matching_result.append((i,i+len1))
			if adjacent_character + str1 == str2[len2-len1-1:len2]:
				matching_result.append((len2-len1,len2))
			return matching_result

def rabin_karp_matcher(str1,str2,q=13,adjacent_character=None,chara2num=None):
	'''

	:param str1: searching string
	:param str2: database string
	:param q: a prime number, used to do modular arithmetic
	:param adjacent_character: expected character next to pattern of str1 in str2
	:return: the span list where str1 matches sub-str2
	'''
	'''
	not yet implement the adjacent_character
	'''
	matching_result = []
	if not str1 or not str2:
		return matching_result
	if len(str1) > len(str2):
		return matching_result
	if chara2num is None:
		chara_set = set(str1+str2) if adjacent_character is None \
					else set(str1+str2+adjacent_character)

		chara2num = {}
		count = 0
		for chara in chara_set:
			chara2num[chara] = count
			count += 1
		d = count
	else:
		d = len(chara2num)
	len1 = len(str1)
	len2 = len(str2)
	if adjacent_character is None:
		h = 1
		for _ in range(len1-1):
			h = (h*d)%q
		p = 0
		t = 0
		for i in range(len1):
			p = (d*p+chara2num[str1[i]])%q
			t = (d*t+chara2num[str2[i]])%q
		for i in range(len2-len1+1):
			if p == t:
				if str1 == str2[i:i+len1]:
					matching_result.append((i,i+len1))
			if i < len2-len1:
				t = (d*(t-chara2num[str2[i]]*h) + chara2num[str2[i+len1]])%q
		return matching_result


####### for automaton matcher #######
def is_suffix(str1,str2):
	if not str1:
		return True
	if len(str2) < len(str1):
		return False
	for i in range(1,len(str1)+1):
		if str1[-i] != str2[-i]:
			return False
	return True
def compute_transition_function(pattern:str,input_alphabet):
	transition_function = {}
	m = len(pattern)
	for q in range(m+1):
		for a in input_alphabet:
			k = min(m,q+1)
			while not is_suffix(pattern[0:k],pattern[0:q]+a):
				k -= 1
			transition_function[(q,a)] = k
	return transition_function

def finite_automaton_matcher(str1,str2,trans_func=None,m=None):
	'''
	:param str1: searching string
	:param str2: database string
	:param trans_func: transition function
	:param m: accepting state
	:return: the span list where pattern matches sub-text
	'''
	matching_result = []
	if not str1 or not str2:
		return matching_result
	if len(str1) > len(str2):
		return matching_result
	if len(str1) == len(str2):
		if str1 == str2:
			matching_result.append((0,len(str1)))
		return matching_result
	if trans_func is None:
		trans_func = compute_transition_function(str1,set(str1+str2))
	if m is None:
		m = max(trans_func.values())
	state = 0
	for i in range(len(str2)):
		state = trans_func[(state,str2[i])]
		if state == m:
			matching_result.append((i-m+1,i+1))
	return matching_result


####### for Knuth-Morris-Pratt matching algorithm #######
def compute_prefix_function(pattern):
	m = len(pattern)
	shift_transition = {}
	shift_transition[1] = 0
	k = 0
	for q in range(2,m+1):
		while k > 0 and pattern[k] != pattern[q-1]:
			k = shift_transition[k]
		if pattern[k] == pattern[q-1]:
			k += 1
		shift_transition[q] = k
	return shift_transition

def kmp_matcher(str1,str2,shift_transition=None):
	'''
	:param str1: searching string, also called pattern
	:param str2: database string
	:return: the span list where pattern matches sub-text
	'''
	matching_result = []
	if not str1 or not str2:
		return matching_result
	if len(str1) > len(str2):
		return matching_result
	if len(str1) == len(str2):
		if str1 == str2:
			matching_result.append((0, len(str1)))
		return matching_result
	len1 = len(str1)
	len2 = len(str2)
	if shift_transition is None:
		shift_transition = compute_prefix_function(str1)
	q = 0 # number of characters matched
	for i in range(1,len2+1): # scan the text from left to right
		while q > 0 and str1[q] != str2[i-1]:
			q = shift_transition[q]
		if str1[q] == str2[i-1]:
			q += 1
		if q == len1:
			matching_result.append((i-len1,i))
			q = shift_transition[q]
	return matching_result

'''
example
str1 = 'ad'
str2 = 'ad, kfad. dc ad .'
print(naive_string_matcher(str1,str2))
print(rabin_karp_matcher(str1,str2))
print(finite_automaton_matcher(str1,str2))
print(kmp_matcher(str1,str2))
'''
