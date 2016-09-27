import cgi, os, cgitb, re, csv
import zipfile as zip
import time as t


####################

cgitb.enable(display = 0, logdir="cgi/error")

form = cgi.FieldStorage()
t1= t.time()

###header##

print(
	"""\
	Content-Type: text/html\n
	<html>
	<head>
		<title>Upload Status</title>
		<link href="../css/main.css" rel="stylesheet">
	</head>
	<body>
	<div class="result">
	"""
	)

##########Source#####

def read_zip_file(filepath):
    zfile = zip.ZipFile(filepath, "r")
    n_list = []
    for finfo in zfile.infolist():
        ifile = zfile.open(finfo)
        n_list.append(ifile.readlines())
    return n_list
if "filen" not in form:
	print("<p>Please upload a zip file!</p>")
else :
	try:
		upfile = form['filen']
		fn = os.path.basename(upfile.filename)
		fnn = re.sub('.zip', '',fn)
		open("zip/" + fn, "wb").write(upfile.file.read())
		zipf = "zip/"+fn
		nl = sum(read_zip_file(zipf), [])
		for i in range(len(nl)):
			nl[i] = str(nl[i])
			nl[i] = re.findall("\d+",nl[i])
			
		nl = sum(nl,[])	
		odd = 0
		even = 0
		for i in range(len(nl)):
			nl[i]=  int(nl[i])
			if nl[i]%2==0:
				even+=1
			else:
				odd+=1
		nsum = sum(nl)
		count = len(nl)
		spd = 0
		if nsum >1000:
			spd = 1

		#csv create code
		data = [['Sum', nsum],["Count", count], ["Odd Digits", odd], ["Even Digits", even], ["Special Digit", spd]]
		cfile = csv.writer(open("csv/"+fnn+".csv", "w"))
		for i in data:
			cfile.writerow(i)
		t2 = t.time()
		tt = t2-t1

		

		print("""
			<p>Sum: %d</p>
			<p>Count: %d </p>
			<p>Odd Digits: %d </p>
			<p>Even Digits: %d </p>
			<p>Special Digit: %d </p>
			<b>File saved:  <a href="../csv/%s.csv">  (Download: %s.csv)</a><b><hr>
			<b><small>Calculated in time: %2f seconds</p><br> &copy; Paras Sharmaa<b>
			
			""" %(nsum, count, odd, even, spd, fnn,fnn, tt))
	except:
		print("Error Processing. Systems thinks that zip file do not contain txt files with numbers or the file is corrupt!!")	


   

print(
	"""
	</div>
	</body>
	</html>
	"""
	)
   
