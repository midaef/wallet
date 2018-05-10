
import datetime
import hashlib
import MySQLdb
import string
import random
import webbrowser


def addmoney():
	t = 0
	wallets = []
	print('Add money to wallet')
	print('1.Qiwi')
	value = input('Input value: ')
	w = getwallets()
	for i in w:
		wallets.append([i[1], i[4]])
	print('\nWallets:' + ' ' * 29 + 'Balance:')
	for j in wallets:
		t+=1
		print(str(t) + ')' + j[0] + ' ' * 2 + str(j[1])) 
	print('')
	wal = int(input('Input wallets: ')) - 1
	print('Chose wallet: ' + wallets[wal][0])
	if value == '1':	
		webbrowser.open_new_tab('https://qiwi.me/')#сылка на ваш киви кошелек	


def getwallets():
	login = 'stdian'
	conn = condb()
	cursor = conn.cursor()
	query = "SELECT * FROM wallets WHERE login = "  + '"' + login + '"'
	connection = condb()
	cursor = connection.cursor()
	cursor.execute(query)
	data =  cursor.fetchall()
	cursor.close()
	connection.close()
	return data


def condb():
	connection = ''
	try:
		connection = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '1234', db = 'chat', charset = 'utf8')
	except:
		print('Connect ERROR!\nCheck internet connection')
		exit()
	return connection


def createwallet():
	s = []
	login = 'stdian'
	for i in string.ascii_lowercase:
		s.append(i)
	for i in string.ascii_uppercase:
		s.append(i)
	for i in range(0, 10):
		s.append(str(i))
	sts = ''
	for i in range(0, 33):
		sts = sts + s[random.randrange(0, len(s) - 1)]
	

	conn = condb()
	cursor = conn.cursor()
	reg = "SELECT wallet FROM wallets WHERE wallet = '" + sts + "'"
	cursor.execute(reg)
	data =  cursor.fetchall()
	cursor.close()
	conn.close()
	if data != ():
		createwallet()
	else:
		if len(getwallets()) < 5:
			print('Successful created wallet!')
			reg = "INSERT INTO wallets(wallet, login, hash) VALUES(%s,%s,%s)"
			h = login + sts
			h = str(hashlib.md5(h.encode("utf-8")).hexdigest())
			args = (str(sts), str(login), str(h))
			connection = condb()
			# log('SYSTEM', 'Registeration', 'login: '  + login, connection)
			cursor = connection.cursor()
			cursor.execute(reg, args)
			cursor.close()
			connection.commit()
			connection.close()
		else:
			print('Too money wallets!')


if __name__ == '__main__':
	createwallet()
	#getwallets()
	addmoney()