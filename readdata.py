import os
import pymongo


os.system("git clone https://github.com/PrajwalPmahale/clamav.git")
os.system("mkdir -p clamavdatabase")
os.system("tar -xvzf clamav/daily.tar.gz -C /clamsetup/clamavdatabase/")
os.system("tar -xvzf clamav/dhsb.tar.gz -C /clamsetup/clamavdatabase/")

os.system("tar -xvzf clamav/main.tar.gz -C /clamsetup/clamavdatabase/")

bad_files=["main.hsb","main.hdb","daily.hsb","daily.hdb","daily.hdu"]
good_files=["main.fp","daily.fp"]

def parse_file(filename,coll):
	fp=open("clamavdatabase/"+filename)
	hashes = []
	while True:
		line=fp.readline()
		if not line:
			if len(hashes)>0:
				coll.insert_many(hashes)
			break
		signature = line.strip().split(":")
		hashes.append({"name":signature[2],"hash":signature[0]})
		if len(hashes)==1000000:
			coll.insert_many(hashes)
			print("inserted "+ str(len(hashes))+" signatures from "+ filename)
			hashes=[]

	fp.close()
	print("Finished parsing "+ filename)


client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["clamav"]

for bad_file in bad_files:
	print("Reading "+bad_file)
	parse_file(bad_file,db["bad_files_md5"])

for good_file in good_files:
	print("Reading "+good_file)
	parse_file(good_file,db["good_files_md5"])
