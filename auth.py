#coding:utf-8

import re
import os
import tornado.ioloop
import tornado.web
from setting import db


def get_tags(content):
	r = re.compile(ur"@([\u4E00-\u9FA5\w-]+)")
	return r.findall(content)

class BaseHandler(tornado.web.RequestHandler):
		def get_current_user(self):
			return self.get_secure_cookie("user")


class WeiboHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("weibo_add.html")


	@tornado.web.authenticated
	def post(self):
		result = self.get_argument("content","")
		for i in get_tags(result):
			print i
		db.weibo.insert({"content":result,"user":self.get_current_user()})
		self.write(result)


class MainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.redirect("/user")

class RegisterHandler(BaseHandler):
	def get(self):
		self.render("register.html")

	def post(self):
		account = self.get_argument("account")
		password = self.get_argument("password")
		if account == "" or password == "" :
			return self.write("account or password no writer")

		if db.user.find({"account":account}).count() > 0 :
			return self.write("account is registered！")
		db.user.insert({"account":account,"password":password})
		self.set_secure_cookie("user", account)
		self.redirect("/user")
		
class UserInfoHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.get_current_user()
		self.render("userinfo.html",**{"user":user})
		


class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")

	def post(self):
		account = self.get_argument("account")
		password = self.get_argument("password")
		self.write(account)
		if account == "" or password == "" :
			return self.write("账号或密码未填写")

		user = db.user.find_one({"account":account},{"account":1,"password":1})

		if not user :
			return self.write("木有该账号")

		if user["password"] != password:
			return self.write("密码错误")
		# if db.user.find({"account":account}).count() == 0 :
		# 	return self.write("木有该账号")
		# if db.user.find({"account":account,"password":password}).count() == 0:
		# 	return self.write("密码错误")
		self.set_secure_cookie("user", user["account"])
		self.redirect("/")


class BingSchoolHandler(BaseHandler):
	def get(self):
		self.render("bindschool.html")

	def post(self):
		school_name = self.get_argument("school_name")
		student_id = self.get_argument("student_id")

		if school_name == "" or student_id == "" :
			return self.write("学校名或学号未填写！")

		db.school.insert({"school_name":school_name,"student_id":student_id})

		self.redirect("/")

class IssueHandler(BaseHandler):
	def get(self):
		self.render("issue.html")

	def post(self):
		task = self.get_argument("task")
		tel = self.get_argument("tel")
		self.write(task)
		if not task :
			return self.write("任务未填写！")
		if not tel :
			return self.write("电话未填写！")
		
		db.issue.insert({"task":task,"tel":tel})
		self.redirect("/")

class TaskSuccessHandler(BaseHandler):
	def get(self):
		self.render("tasksuccess.html")

class TaskUnsuccessHandler(BaseHandler):
	def get(self):
		self.render("taskunsuccess.html")

class FindHandler(BaseHandler):		#发布任务判断当前user是否为空。为空则跳转到绑定学号页面
	@tornado.web.authenticated
	def get(self):
		user = self.get_current_user()
		issue = db.issue.find()
		if user != "" :
			self.render("find.html",**{"issue":issue})
		self.redirect("/bindschool")


class ReceiveHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		task = self.get_argument("task",None)
		issue = db.issue.find()
		self.render("receive.html",**{"issue":issue})

settings = {
			"cookie_secret":"61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			"login_url":"/login",
			#"static_path":os.path.join(os.path.dirname(__file__), "static"),,
			"template_path":os.path.join(os.path.dirname(__file__), "templates"),
			"debug":True			
	}

application = tornado.web.Application([
	(r"/",MainHandler),
	(r"/login",LoginHandler),
	(r"/register",RegisterHandler),
	(r"/weibo/add",WeiboHandler),
	(r"/user",UserInfoHandler),
	(r"/bindschool",BingSchoolHandler),
	(r"/issue",IssueHandler),
	(r"/tasksuccess",TaskSuccessHandler),
	(r"/taskunsuccess",TaskUnsuccessHandler),
	(r"/find",FindHandler),
	(r"/receive",ReceiveHandler),
], **settings)

if __name__ == "__main__":
	application.listen(7777)
	tornado.ioloop.IOLoop.instance().start()
		
		