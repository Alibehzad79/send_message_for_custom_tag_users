from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os, instaloader, time, random, ast

# dir address / path
dir_path = os.getcwd() + '/'

# real path for webdriver service
PATH = str(dir_path) + 'chromedriver'

# set service
service = Service(PATH)

# chrome options
options = Options()

# set deriver
driver = webdriver.Chrome(options=options, service=service)

# urls
instagram_login_url = 'https://instagram.com/'

# set xpath elements from instagram

	# login Xpaths
username_xpath = '//input[@name="username"]'
password_xpath = '//input[@name="password"]'
submit_button =  '//button[@type="submit"]'

	# send message Xpaths
# notification_xpath = '/html/body/div[5]/div/div/div/div[3]/button[2]'	
notification_xpath = '//*[contains(text(), "Not Now")]'	
# send_message_button_xpath = '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button'	
# text_input_section_xpath = '/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]'
text_input_xpath = '//input[@name="queryBox"]'
# select_username_xpath = '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]'
# next_button_xpath = '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/button'
# textarea_section_xpath = '_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9o  _abbh'
textarea_xpath = '//textarea[@placeholder="Message..."]'
# send_button_xpath = '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'


# get to website address

class Bot:
	# login instagram
	def instagram_login(self, username, password):
		print('login instagram.com')
		driver.get(instagram_login_url)
		time.sleep(10)
		try:
			username_field = driver.find_element(By.XPATH, username_xpath)
			time.sleep(5)
			username_field.send_keys(username)
			time.sleep(1)
		except Exception as e:
			print('username_field not found')	
		try:	
			password_field = driver.find_element(By.XPATH, password_xpath)
			time.sleep(5)
			password_field.send_keys(password)
			time.sleep(1)
		except Exception as e:
		 	print('password_field not found')

		try: 			
			submit_field = driver.find_element(By.XPATH, submit_button)
			time.sleep(5)
			submit_field.click()
			time.sleep(10)
		except Exception as e:
			print(e)	
		if 'Save Your Login Info?' in driver.page_source:
			print('Login Successful ' + username)
			driver.get(instagram_login_url + username + '/')
			return True
		else:
			print('Account is Disabel or error in internet Connection')
			with open('disabel_accounts.txt', 'a') as f:
				f.write(f'{username} : {password} \n')
	# logout from instagram account
	def instagram_logout(self):
		print('logouting ...')
		driver.get(instagram_login_url + "accounts/logout/")			

	# extract user from tag
	def extract_user_from_tag(self, L):
		with open('tags.txt', encoding='utf-8') as tags:
			tags = tags.read().split('\n')
			if tags[-1] == '':
				del tags[-1]
			del tags[0]
			user_list = []
			if tags is not None or tags != '':
				print(tags)
				for tag in tags:
					try:
						hashtag = instaloader.Hashtag.from_name(L.context, tag)
					except Exception as e:
						print(e)
						continue
					
					for post in hashtag.get_posts():
						try:
							profile = instaloader.Profile.from_username(L.context, post.owner_username)
						except Exception as e:
							print(e)
							continue	
						with open('targets_done.txt') as targets_done:
							targets_done = targets_done.read().split('\n')
							if profile.username not in targets_done and profile.username not in user_list:
								follower_count = profile.get_followers().count
								if 100 < int(follower_count) < 10000:
									user_list.append(profile.username)
									print(f'{profile.username}: added to target list')
									if len(user_list) == 2:
										print('Extract Done!')
										break
								else:
									print(f'{profile.username}: skip')	
							else:
								print('target is in targets_done.txt')
								continue		

				if len(user_list) > 0:
					return user_list
				else:
					print('user_list is empty')
					return None				
			else:
				print('tags.txt is not found, please create tags.txt file')	

	def send_message(self, target_list):
		with open('message.txt') as message:
			message = message.read()
			if message is not None or message != '':
				if target_list is not None:
					for target in target_list:
						driver.get(instagram_login_url + 'direct/inbox/')
						time.sleep(10)
						try:
							notification = driver.find_element(By.XPATH, notification_xpath)
							time.sleep(5)
							notification.click()
							time.sleep(1)
						except Exception as e:
							print('notification is not found')	
						driver.get(f'{instagram_login_url}direct/new/')	
						time.sleep(1)	
						try:
							text_input = driver.find_element(By.XPATH, text_input_xpath)
							time.sleep(5)
							text_input.send_keys(target)
							time.sleep(20)
						except Exception as e:
							print('text_input is not found')	
						try:
							select_username = driver.find_element(By.XPATH, f'//div[contains(text(), "{target}")]')
							time.sleep(5)
							select_username.click()
							time.sleep(5)
						except Exception as e:
							print('select_username is not found')	
						try:
							next_button = driver.find_element(By.XPATH, f'//div[contains(text(), "Next")]')	
							time.sleep(5)
							next_button.click()
							time.sleep(10)	
						except Exception as e:
							print('next_button is not found')			
						try:
							textarea = driver.find_element(By.XPATH, textarea_xpath)
							time.sleep(5)
							textarea.click()
							textarea.send_keys(message + Keys.ENTER)
							time.sleep(20)
							with open('targets_done.txt', 'a') as targets_done:
								targets_done.write(target + '\n')
							driver.get(instagram_login_url + 'direct/inbox/')
							x = random.randint(120, 140)
							print(f'sleep for {str(x)} seccond')
							time.sleep(x)		
						except Exception as e:
							print('textarea is not found')									
			else:
				print('message.txt is empty or message.txt is not found, please create message.txt file')								
	def start(self, L):
		with open('accounts.txt', encoding='utf-8') as accounts:
			accounts = accounts.read().split('\n')
			if accounts[-1] == '':
				del accounts[-1]
			if accounts is not None or accounts != '':
				for account in accounts:
					new_account = ast.literal_eval(account)
					username = new_account.get('username')
					password = new_account.get('password')

					if self.instagram_login(username, password):
						target_list = self.extract_user_from_tag(L)
						self.send_message(target_list)
						self.instagram_logout()
						print('------------------------------------')




os.system('clear')
user = 'username' # just one instagram account
password = 'password'
status = False
try:
	L = instaloader.Instaloader()
	L.login(user, password)
	print('instaloader Login successful')
	status = True
except:
	print('instaloader Login field!')
	status = False				

bot = Bot()
if status:
	bot.start(L)
	L.close()
else:
	print('instaloader Login field!')
