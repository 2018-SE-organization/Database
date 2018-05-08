#<summary> A function, that mask class time format into bitstring </summary>
#<param name="str"> class time </param>
#<returns> 19 length bitstring </returns>
#<exp> timeMask(二78) = ['0100000000000110000'] </exp>

# day AB 1234 CD 5678 EFGH
# 000 00 0000 00 0000 0000
# where 一  二  三  四  五
#      001 010 011 100 101

def timeMask(str):
	result = []
	dict = {
		"一": '001',
		"二": '010',
		"三": '011',
		"四": '100',
		"五": '101',
		"A" : 0,
		"B" : 1,
		"1" : 2,
		"2" : 3,
		"3" : 4,
		"4" : 5,
		"C" : 6,
		"D" : 7,
		"5" : 8,
		"6" : 9,
		"7" : 10,
		"8" : 11,
		"E" : 12,
		"F" : 13,
		"G" : 14,
		"H" : 15,
	};
	
	arr = ""
	cur = []
	for i in str:
		if i == '一' or i == '二' or i == '三' or i == '四' or i =='五':
			if arr != "":
				#	turn back to string then add strings
				result += [''.join(cur)]
			arr = ''.join(["0" for x in range(16)])
			arr = dict[i] + arr;
			#	turn string to current char array
			cur = list(arr)
		else:
			cur[dict[i] + 3] = '1'
	result += [''.join(cur)]
		
	return result
