import json
import random

# 预设值
USER_FILE = 'user.json'
CASE_FILE = 'TotalCases.json'
INIT_SCORE = 200
RANK_SCOPE = 100
CASE_TYPES = ['字符串', '线性表', '数组', '查找算法','排序算法', '数字操作', '树结构', '图结构']
GROUP_MAX_SCORE = 2500
GROUP_MAX_NUM = 5

# 全局变量
DATA_USERS = {}
DATA_CASES = {}
USER_NAME = ''


def getUserData():
	f = open(USER_FILE, encoding='utf-8')
	return json.loads(f.read())


def getCaseData():
	f = open(CASE_FILE,encoding='utf-8')
	return json.loads(f.read())


def updateUserData():
	with open(USER_FILE, 'w') as f:
		json.dump(DATA_USERS, f)


def addAccount(name):
	evaluate = []
	for i in CASE_TYPES:
		evaluate.append({i: 0})
	DATA_USERS[name] = {'user_name': name, 'rank_score': INIT_SCORE,'type_evaluate':evaluate, 'records': []}
	updateUserData()


def register():
	name = input("输入一个新名字: ")
	while name in DATA_USERS.keys():
		name = input("这个名字已经被占用，请输入一个新名字: ")
	addAccount(name)
	return name


def login():
	print("欢迎使用编程学习系统")
	flag = input("已经有账号了?(y/n) ")
	
	while flag != 'y' and flag != 'n':
		flag = input("输入‘y’或者‘n’: ")
	
	if flag == 'n':
		return register()
	else:
		name = input("请输入你的账号名: ")
		while name not in DATA_USERS.keys():
			name = input("该账号名不存在，请重新输入： ")
		return name


def getRecommendCase(type, offset):
	base = DATA_USERS[USER_NAME]['rank_score'] + offset
	has_done_case = list(map(lambda x: x['case_id'], DATA_USERS[USER_NAME]['records']))
	enabled_cases = list(filter(lambda x: x['case_id'] not in has_done_case, filter(lambda x: x['case_type'] == CASE_TYPES[type],DATA_CASES)))
	scoped_cases = list(filter(lambda x: base - RANK_SCOPE< x['case_score'] < base + RANK_SCOPE, enabled_cases))
	enabled_cases = list(filter(lambda x: base + RANK_SCOPE < x['case_score'] < base - RANK_SCOPE, enabled_cases))
	
	res_cases = []
	
	while sum(map(lambda x:x['case_score'], res_cases)) < GROUP_MAX_SCORE and len(res_cases) < GROUP_MAX_NUM and len(scoped_cases) > 0:
		random_pos = int(random.random()*len(scoped_cases))
		res_cases.append(scoped_cases[random_pos])
		del scoped_cases[random_pos]
	
	backup_cases = []
	if sum(map(lambda x:x['case_score'], res_cases)) < GROUP_MAX_SCORE and len(res_cases) < GROUP_MAX_NUM:
		for i in range(len(enabled_cases)):
			diff = abs(base - enabled_cases[i]['case_score'])
			if len(backup_cases) < GROUP_MAX_NUM - len(res_cases):
				backup_cases.append((i, diff))
			else:
				backup_cases.sort(key=lambda x:x[1],reverse=True)
				if diff < backup_cases[0]:
					backup_cases[0] = (i, diff)
		backup_cases.sort(key=lambda x: x[1])
	
	while sum(map(lambda x:x['case_score'], res_cases)) < GROUP_MAX_SCORE and len(res_cases) < GROUP_MAX_NUM and len(backup_cases) > 0:
		res_cases.append(enabled_cases[backup_cases[0][0]])
		del backup_cases[0]
	
	return res_cases


def getOffset(evaluate):
	return 0


def test():
	print("测试题目难度会根据你的分数确定，并会采取计时来综合评估你的成绩，请注意做题时间")
	input("已准备好按Enter键即可开始")
	random_type = int(random.random()*len(CASE_TYPES))
	evaluate = DATA_USERS[USER_NAME]['type_evaluates'][CASE_TYPES[random_type]]
	case = getRecommendCase(random_type, getOffset(evaluate))[0]
	print("测试题目：")
	print("     种类："+case['case_type'])
	print("     下载地址："+case['case_zip'])
	pass


def exercise():
	print("练习题目不会计时，将会根据你的意愿以及做题记录确定题目种类，并会根据你的分数确定难度")
	print("请选择你的做题倾向：")
	print("可选种类：1.字符串, 2.线性表, 3.数组, 4.查找算法，6.排序算法 5.数字操作, 7.树结构, 8图结构.")
	type = int(input("请输入对应编号（1-8）："))-1
	
	cases_eva = DATA_USERS[USER_NAME]['type_evaluates']
	sorted_types = list(map(lambda x: CASE_TYPES.index(x), sorted(cases_eva.keys(), key=lambda x: cases_eva[x])))
	if sorted_types[0] != type:
		rec_type = sorted_types[0]
	else:
		rec_type = sorted_types[1]
	cases = getRecommendCase(type, getOffset(cases_eva[CASE_TYPES[type]])) + getRecommendCase(rec_type, getOffset(cases_eva[CASE_TYPES[rec_type]]))
	
	print("系统为您推荐以下练习题目：")
	for i in range(len(cases)):
		print(" 题目"+str(i+1)+"：")
		print("     种类：" + cases[i]['case_type'])
		print("     下载地址：" + cases[i]['case_zip'])
		
	pass


def start():
	print("成功进入系统!")
	print("请选择进行测试或者练习（测试可以提高用户的编程评估分，从而有可能被推送到难度更高的题目，练习则不影响评估分)")
	flag = input("（回复‘E’表示练习，‘T’表示测试）：")
	while flag != 'T' and flag != 'E':
		flag = input("请输入‘T’或者‘E’")
	if flag == 'T':
		test()
	else:
		exercise()


if __name__ == '__main__':
	DATA_USERS = getUserData()
	DATA_CASES = getCaseData()
	USER_NAME = login()
	start()
