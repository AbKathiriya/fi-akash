import os
import time
import datetime
import subprocess

#print "enter the folder name"
#name = raw_input()
print "the current directory is", os.getcwd()
os.chdir('/Users/karthikeyan/Desktop/cases/')
#os.mkdir(name)
cwd = os.getcwd()
print "the directory created and the path is", os.getcwd()
# print os.path.getsize(os.getcwd())
today = datetime.date.today()
print 'Current system date is %s :'%today
zipped = 0
skipped = 0
total = 0
remaining =0
for items in os.listdir(cwd):
	total += 1
	stat = os.stat(items)
	ctime = stat.st_birthtime
	ctime = datetime.datetime.fromtimestamp(int(ctime)).strftime('%Y-%m-%d')
	ctime = datetime.datetime.strptime(ctime, '%Y-%m-%d').date()
	days = int((today - ctime).days)
	if items == "archive" or ".DS_Store" in items or "tar.gz" in items:
		skipped += 1
		continue
	if days >= 60:
		zipped += 1
		fname = str(items)+'.tar.gz'
		DEVNULL = open(os.devnull, 'wb')
		subprocess.call(['tar', '-zcvf', fname, items], stdout = DEVNULL)
		print 'New zip file %s created successfully!!'%fname
		subprocess.call(['mv',fname,cwd+'/archive'])
		print 'File %s moved to archive folder successfully!!'%fname
		subprocess.call(['rm','-r',items])
		print 'Root folder %s deleted successfully'%items
	else:
		remaining += 1
print "Total : %s \n Zipped : %s \n Skipped : %s \n Remaining : %s" % (total,zipped,skipped,remaining)
