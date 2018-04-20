from phase2 import get_all_tweets
import os

handles = ['katyperry','realDonaldTrump','ManUtd','justinbieber','taylorswift13',
			'ladygaga','TheEllenShow','Cristiano','YouTube','jtimberlake','twitter',
			'KimKardashian','britneyspears','ArianaGrande','ddlovato','selenagomez',
			'cnnbrk','shakira','jimmyfallon','BillGates']

for user in handles:
	get_all_tweets("@"+user, user + ".mp4", user + ".json")

while(True):
	try:
		for n in range(20):
			os.remove(str(n) + ".jpg")
	except:
		break