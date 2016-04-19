#_*_ coding: utf-8 _*_

#导入re模块
import re

#将正则表达式编译成Pattern对象，注意hello前面的r的意思是“原生字符串”


#使用re.match匹配文本，获取匹配结果，无法匹配是将返回None
result1 = re.match(r"hello",'hello')
result2 = re.match(r"hello",'hell7')
result3 = re.match(r"hello",'wwwhello')
result4 = re.match(r"hello",'hello hsh')

#使用search（）查找匹配的子串，不存在能匹配的子串是将返回None
result5 = re.search(r"world",'hello world !')

#按照能够匹配的子串将string分割后返回列表
result6 = re.split(r'\d+','one1two2three3four4')

#以列表的形式返回全部能匹配的子串
result7 = re.findall(r'\d+','one1two2three3four4')

#返回一个顺序访问每一个匹配结果的迭代器。
for m in re.finditer(r'\d+','one1two2three3four4'):
	print m.group(),
#sub 替换
s = 'i say , hello world!'
print re.sub(r'(\w+) (\w+)',r'\2 \1',s)
print re.subn(r'(\w+) (\w+)',r'\2 \1',s)

def func(m):
	return m.group(2).title() + ' ' + m.group(1).title()	

print re.sub(r'(\w+) (\w+)',func,s)
print re.subn(r'(\w+) (\w+)',func,s)

#如果result1匹配成功
if result1:
	print result1.group()
else:
	print '1匹配失败'

#如果result2匹配成功
if result2:
	print result2.group()
else:
	print '2匹配失败'
#如果result3匹配成功
if result3:
	print result3.group()
else:
	print '3匹配失败'
#如果result4匹配成功
if result4:
	print result4.group()
else:
	print '4匹配失败'
#如果result5匹配成功
if result5:
	print result5.group()
else:
	print '5匹配失败'
#如果分割成功
if result6:
	print result6
else:
	print '6分割失败'

#如果搜索成功
if result7:
	print result7
else:
	print '7搜索失败'	




