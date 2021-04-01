# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import dotenv_values
from datetime import datetime, date
import time

# 該 flag 是為了讓簽到和簽退只做一次並輪替
isPunchingIn = False
isPunchingOut = False

chromeOptions = Options()
chromeOptions.headless = True # 隱藏網頁


# 讀取 Portal 帳號資訊
def loadProfile(profile):
	values = dotenv_values(".env")
	profile.account = values["ACCOUNT"]
	profile.password = values["PASSWORD"]
	profile.webdriver_path = values["WEBDRIVER_PATH"]
	profile.startTime = {"HOUR": values["START_TIME"].split(':')[0], "MIN": values["START_TIME"].split(':')[0]}
	profile.endTime = {"HOUR": values["END_TIME"].split(':')[0], "MIN": values["END_TIME"].split(':')[0]}
	profile.hours = int(values["HOURS"])
	return profile


# 儲存 Portal 帳號資訊
class Profile():
	def __init__(self, account = None, password = None):
		self._account = account
		self._password = password

	@property
	def account(self):
		return self._account

	@property
	def password(self):
		return self._password

	@property
	def webdriver_path(self):
		return self._webdriver_path

	@property
	def startTime(self):
		return self._startTime

	@property
	def endTime(self):
		return self._endTime

	@property
	def hours(self):
		return self._hours

	@account.setter
	def account(self, account):
		self._account = account

	@password.setter
	def password(self, password):
		self._password = password

	@webdriver_path.setter
	def webdriver_path(self, webdriver_path):
		self._webdriver_path = webdriver_path

	@startTime.setter
	def startTime(self, startTime):
		self._startTime = startTime

	@endTime.setter
	def endTime(self, endTime):
		self._endTime = endTime

	@hours.setter
	def hours(self, hours):
		self._hours = hours
	

# 簽到
def punchIn(driver):
	attendWork = driver.find_element_by_id('AttendWork')
	attendWork.send_keys("TA")
	driver.find_element_by_xpath("//button[contains(@id, 'signin')]").click()
	isPunchingOut = False

# 簽退
def punchOut(driver):
	time.sleep(uniform(5.0, 10.0)*60) # random delay
	driver.find_element_by_xpath("//button[contains(@id, 'signout')]").click()
	isPunchingIn = False

# 登入流程
def personnelSystemPunchIn(driver, profile, punchFunc):
	# 登入
	personnelSystemUrl = "https://cis.ncu.edu.tw/HumanSys/home"
	driver.get(personnelSystemUrl)
	driver.find_element_by_link_text("登入").click()

	# 輸入 protal 帳號
	inputAccount = driver.find_element_by_id('inputAccount')
	inputPassword = driver.find_element_by_id('inputPassword')
	inputAccount.send_keys(profile.account)
	inputPassword.send_keys(profile.password)
	inputPassword.submit()

	# 進入打卡頁面
	driver.find_element_by_xpath("//button[contains(@class, 'btn btn-primary')]").click()
	driver.get("https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId=149102")

	# 執行簽退或是簽到
	punchFunc(driver)

	# 關閉的原因是 session 會記住帳號資訊，使得登入流程被省略。然後這樣會跟程式寫的流程不同而出錯，但我懶得改所以就都關掉 ：）
	driver.close()


# 查看目前時間有沒有符合 timeStamp ，有就回傳 True, 否就回傳 False
def checkTimeForPunching(timeStamp):
	currentTime = datetime.now()
	year = int(currentTime.strftime("%Y"))
	month = int(currentTime.strftime("%m"))
	day = int(currentTime.strftime("%d"))
	week = date(year, month, day).isoweekday()

	if(week == 6 or week == 7):
		return False

	if(currentTime.strftime("%H") == timeStamp["HOUR"] and currentTime.strftime("%M") == timeStamp["MIN"]):
		return True
	else:
		return False



if __name__ == '__main__':
	punchTime = 0
	totalWorkTime = 0

	profile = Profile()
	profile = loadProfile(profile)

	print(profile.__dict__)

	driver = webdriver.Chrome(profile.webdriver_path, options=chromeOptions)

	while True:
		if(checkTimeForPunching(profile.startTime) and isPunchingIn == False):
			print("[ 簽到 ]")
			isPunchingIn = True
			personnelSystemPunchIn(driver, profile, punchIn)
			punchTime = datetime.now().strftime("%H")
			

		if(checkTimeForPunching(profile.endTime) and isPunchingOut == False):
			print("[ 簽退 ]")
			isPunchingOut = True
			personnelSystemPunchIn(driver, profile, punchOut)

			workTime = datetime.now().strftime("%H") - punchTime
			print("(ˊ～ˋ)辛苦了，本次打卡時數為 ", workTime, " 小時\n")
			totalWorkTime += workTime
			print("\t=> 總計時數為 ", totalWorkTime, " 小時")


		if(totalWorkTime == profile.hours):
			break










