#coding=utf-8
import requests
from bs4 import BeautifulSoup
import threading
import re
import json
import codecs
import time
from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import os
import inspect
import ctypes
import queue
import shutil
'''
class video_downloader():
	def __init__(self,url):
		self.server="http://api.xfsub.com"
		self.api="http://api.xfsub.com/xfsub_api/?url="
		self.get_url_api="http://api.xfsub.com/xfsub_api/url.php"
		self.url=url.split('#')[0]
		self.target=self.api+self.url
		self.s=requests.session()
	def get_key(self):
		req=self.s.get(url=self.target)
		req.encoding='utf-8'
		self.info=json.load(re.findall('"url.php",\ (.*),',req.text)[0])

'''
start_time=time.time()
#print len(sys.argv)
if len(sys.argv) != 7:
	print "thread default is 20,catalog default is tmp123"
	print "example:"
	print "python vip.py -u http://www.baidu.com -thread 20 -c tmp123"
	print "vip.exe -u http://www.baidu.com -thread 20 -c tmp123"
	print ""
if len(sys.argv) !=3:
	print "python vip.py -u http://www.baidu.com"
	print "vip.exe -u http://www.baidu.com"
	sys.exit()
if len(sys.argv) ==7:
	if sys.argv[4].isdigit():
		num_thread=sys.argv[4]
	dir_name=sys.argv[6]
else:
	num_thread=20
	dir_name="tmp123"
print dir_name
if os.path.exists(dir_name):
	shutil.rmtree(dir_name)
if not os.path.isdir(dir_name):
	os.mkdir(dir_name)
#https://www.iqiyi.com/v_19rrf2nw1g.html

url=sys.argv[2]
#url="https://www.iqiyi.com/v_19rrf2nw1g.html"
count=0
def Handler(pool,point,dir_name,req_url2):
	
	#headers = {'Range': 'bytes=%d-%d' % (start, end-1)}
	#r = requests.get(url, headers=headers, stream=True)
	'''
	for i in filename[start:end]:
		#mutex.acquire()
		#global count
		try:
			r = requests.get("https://cdn.letv-cdn.com/"+str(i).replace("\n",""),stream=True)
			#r = requests.get(url)
			with codecs.open(dir_name+"/"+i.split('/')[5], "wb") as code:
				code.write(r.content)
		except Exception as e:
			continue
		#count =count+1
	'''
	try:
		r = requests.get(req_url2+str(point).replace("\n",""),stream=True)
		#r = requests.get(url)
		with codecs.open(dir_name+"/"+point, "wb") as code:
			code.write(r.content)
	except Exception as e:
		pass
	#print point
	pool.add_thread()
		#print "%.2f%%" % (float(count/float(file_size)) * 100)
		#mutex.release()

		#print("下载进度：%.2f" % (count/len(filename)))
def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)

#线程池
class ThreadPool(object):  #创建线程池类

	def __init__(self, max_num=25):  #创建一个最大长度为20的队列
		self.queue = queue.Queue(max_num)  #创建一个队列
		for i in range(max_num):  #循环把线程对象加入到队列中
			self.queue.put(threading.Thread)  #把线程的类名放进去，执行完这个Queue

	def get_thread(self):  #定义方法从队列里获取线程
		return self.queue.get()  #在队列中获取值

	def add_thread(self):  #线程执行完任务后，在队列里添加线程
		self.queue.put(threading.Thread)



headers = {
	'Connection': 'close',
}

#url=url.replace("://","%3A%2F%2F").replace("/","%2F")
#print url
api="http://www.wq114.org/yun.php?url="+url
#print api
req=requests.get(url=api,headers=headers)
soup=BeautifulSoup(req.content,'lxml')
#print soup("iframe")[0].attrs['src']
url_2=soup("iframe")[0].attrs['src']
api_2="http://www.wq114.org"+url_2
print api_2
rep_2=requests.get(url=api_2,headers=headers)
soup_2=BeautifulSoup(rep_2.content,'lxml')
#print soup_2
s=str((list(soup_2("script"))[5]))
#pattern=re.compile("url	:'(.+)'",re.IGNORECASE)
#url=pattern.findall(s)
#print url
#print s.split(':')[7].split(',')[0].strip(" ").strip("'")
url=s.split(':')[7].split(',')[0].strip(" ").strip("'")
print url
get_data={
	'up':0,
	'url':url
}

res=requests.post(url="http://www.wq114.org/x2/api.php",headers=headers,data=get_data)
print res.content

response=json.loads(res.content)['url'].replace("%3A%2F%2F","://").replace("%2F","/")
print response
print "oooo"
req_url=response.strip("/index.m3u8")+"/"
print req_url
#print "ok"
res=requests.get(url=response,headers=headers)
print res.content
res2=res.content.split('\n')[2]
print res2
#print "ok1"
next_api=req_url+res2
print next_api
req_url2=next_api.strip("/index.m3u8")+"/"
res=requests.get(url=next_api,headers=headers)
#s=res.content.split('\n')
s=res.content
s=s.split('\n')
#print s
#print type(s)
s_list=[]
for i in s[0:]:
	#print i
	if str(i).endswith(".ts"):
		if "/" in i:
			i=i.split('/')[5]
		#print i
		s_list.append(i)
#print s_list
file_size = len(s_list)
print file_size
#num_thread=50
#part = file_size // num_thread
#print part
#Thread_list=[]
p = ThreadPool(20)  #执行init方法；  一次最多执行10个线程
#mutex = threading.Lock()
'''for i in range(file_size):
	start = part * i
	if i == num_thread - 1:
		end = file_size
	else:
		end = start + part
	#print i
	#print("下载进度：%.2f" % (end/float(file_size)))
	'''
count_num=0
for point in s_list[0:]:
	count=count+1
	print("下载进度：%.3f" % (count/float(file_size)*100)).decode('utf-8').encode('gb2312')+"%"
	thread = p.get_thread()  #线程池10个线程，每一次循环拿走一个拿到类名，没有就等待
	t = thread(target=Handler, kwargs={'pool': p,'point':point,'dir_name':dir_name,"req_url2":req_url2})
	#t.setDaemon(True)
	t.start()
	#Thread_list.append(t)

time.sleep(5)

'''main_thread = threading.current_thread()
for t in threading.enumerate():
	if t is main_thread:
		continue'''
#for t in Thread_list[0:]:
	#t.join()

#第二部分 合并ts文件
files2=[]
for root, dirs, files in os.walk(dir_name):
	#print files
	#print type(list(files))
	files=list(files)
try:
	for i in files[:]:
		#print len(files)
		#print files[i]
		if len(i)>len(files[0]):
			#print len(files)
			files2.append(i)
			files.remove(i)
except Exception as e:
	pass
files.sort()
files2.sort()
#print files
#print files2
files=files+files2
#print sorted(files)

#print files

os.chdir(dir_name)
num=len(files)//5
num2=len(files)%5
for i in range(6):
	if i!=5:
		shell_str = '+'.join(files[i*num:(i+1)*num-1])
		shell_str = 'copy /b /y '+ shell_str +" "+str(i)+'.ts'
		print i*num
		print (i+1)*num-1
		#print shell_str
		os.system(shell_str)
	else:
		shell_str = '+'.join(files[5*num:5*num+num2])
		shell_str = 'copy /b /y '+ shell_str +" "+str(5)+'.ts'
		#print shell_str
		print 5*num
		print 5*num+num2
		os.system(shell_str)
shell_str = 'copy /b /y 0.ts+1.ts+2.ts+3.ts+4.ts+5.ts last.mp4'
print shell_str
os.system(shell_str)

#删除文件
os.system("del /Q *.ts")

'''
next_api="http://www.wq114.org/x2/tong.php?url=https://cdn.letv-cdn.com/20181101/SXCSesZ8/index.m3u8"
s=requests.session()
req=s.post(url=next_api)
print req.content

'''
end_time=time.time()
last_time=end_time-start_time
print ("最终耗时：%s 秒" %last_time).decode('utf-8').encode('gb2312')
print ("下载完成,请观看。").decode('utf-8').encode('gb2312')