#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python bot for comment a list of urls in YouTube

import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def youtube_login(email,password):
	try:
		# Browser
		driver = webdriver.Firefox()
		driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')

		# log in
		driver.find_element_by_id('identifierId').send_keys(email)
		driver.find_element_by_id('identifierNext').click()
		WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.NAME, "password")))
		driver.find_element_by_name('password').send_keys(password)
		driver.find_element_by_name('password').send_keys(Keys.ENTER)
		
		
		return driver	
	except :
		print("Erro na parte de login")


def comment_page(driver,urls,commentsCount):
    

	try:
		# Pop a URL from the array	
		url = urls.pop()
		
		# Visite the page	
		driver.get(url)
		

		# Is video avaliable (deleted,private) ?
		if not check_exists_by_xpath(driver,'//*[@id="movie_player"]'):
			return comment_page(driver, urls, random_comment())

		# Scroll, wait for load comment box
		driver.execute_script("window.scrollTo(0, 500);")
		
		# Comments are disabled?
		if check_exists_by_xpath(driver,'//*[@id="comments-disabled-message"]/div/span'):
			return comment_page(driver, urls, random_comment())

		for i in range(commentsCount):
			# Lets wait for comment box
			WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-comment-simplebox-renderer")))
			
			# Activate box for comments
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "simplebox-placeholder")))
			driver.find_element_by_id("simplebox-placeholder").click()

			# Send comment and post
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contenteditable-root")))
			driver.find_element_by_id("contenteditable-root").send_keys(random_comment())
			#driver.find_element_by_id("contenteditable-root").send_keys(Keys.ENTER + Keys.ENTER)
			driver.implicitly_wait(2)
			# Is post ready to be clicked?
			
			driver.find_element_by_id("contenteditable-root").send_keys(Keys.CONTROL + Keys.ENTER)
			print(i+1)
			# Lets wait a bit
			r = np.random.randint(2,5)
			time.sleep(r)
	except:
		print("Erro na hora de envia os comentario")


		
	


def random_comment():

	messages = [
		'S2',
		'GATAA',
		'GATOO',
		'TE AMO',
		'BEST FRIEND EVER',
		'Uhullllll',
		'Casa comigoo',
        'AEEEEEEE', 
		"Parabenss",
		'Nunca duvidei'       
	]
	
	r = np.random.randint(0, len(messages))

	return messages[r]
 
def check_exists_by_xpath(driver,xpath):
	
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True

if __name__ == '__main__':


	#email = 'laerti4325@gmail.com'
	#password = 'kyuubi2012'
	email = input("Digite seu email da conta do youtube\n")
	password = input("Digite sua senha\n")

	#numero de comentarios
	commentsCount = int(input("Quantos comentario deseja fazer?\n")) 

	print("Iniciando")
	print("...")

	# List of Urls
	urls = [
	  'https://www.youtube.com/watch?v=P1v1KcARj-I',	  
	]
	

	# Loga
	driver = youtube_login(email, password)	
	#Espera pagina carregar
	WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "content")))
	# Comentar
	comment_page(driver,urls,commentsCount)
	print("Todos comentarios enviados")
	