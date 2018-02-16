
import re
import csv
import os
import glob
import zipfile
import codecs
#####

########## this can be a single plate data, as well as combined multiple plate data from ENvision###
def read_envision_384_csv(inFile):
    elisa384PlateCount=0
    Single384Dict={}
    rowcount =0
    plate96_listA=[] # A1
    plate96_listB=[] # start with A2
    plate96_listC=[] # start with B1
    plate96_listD=[] # B2

    findBarcode = False
    with open(inFile,'rbU') as csvfile:
        readCSV = csv.reader((x.replace('\0','') for x in csvfile))
        for row in readCSV:
            if len(row) ==0: # ignore empty line
                continue

            if findBarcode == True:
                if elisa384PlateCount >=1:
                    Single384Dict[barcode_name]={0:plate96_listA, 1:plate96_listB, 2:plate96_listC, 3:plate96_listD }
                barcode_name= row[barcode_pos]
                findBarcode = False
                rowcount =0
                plate96_listA=[] # A1
                plate96_listB=[] # start with A2
                plate96_listC=[] # start with B1
                plate96_listD=[] # B2
                elisa384PlateCount += 1
            elif 'Barcode' in row:
                findBarcode = True
                barcode_pos = row.index('Barcode')
            elif len(row) >=24 and row[0]: # find the real data
                rowcount +=1

                for item in row:  ## remove the first column if it is not the data
                    if not '.' in item:
                        row.remove(item)

                for i in range(len(row)):
                    try:
                    	score = float(row[i])
                    except:
                        continue
                    if (i+1)%2 ==1 and rowcount % 2 ==1:
                        plate96_listA.append(score)
                    elif (i+1)%2 ==0 and rowcount %2 ==1:
                        plate96_listB.append(score)
                    elif (i+1)%2 ==1 and rowcount % 2 ==0:
                        plate96_listC.append(score)
                    elif (i+1)%2 ==0 and rowcount % 2 ==0:
                        plate96_listD.append(score)
    print elisa384PlateCount
    if elisa384PlateCount > 0 :
        Single384Dict[barcode_name]={0:plate96_listA, 1:plate96_listB, 2:plate96_listC, 3:plate96_listD }
    else:
        print "Warning! No ELISA data was found!"

    for key in Single384Dict:
        print key
        print Single384Dict[barcode_name][0]
	#print Single384Dict[barcode_name][1]
	#print Single384Dict[barcode_name][2]
	#print Single384Dict[barcode_name][3]
    return Single384Dict  # platenumaber start with 384 barcode

read_envision_384_csv('tmp.csv')
#read_384_csv('Plate2.csv')


###### read all csv files in the file
def combine_csv_dir(infilePath,outfilePath):
    combined_file_name= outfilePath+'/combined.csv'
    combinedfile = open(combined_file_name, 'wb')
    writer = csv.writer(combinedfile)

    if infilePath.endswith(".zip"):
        with zipfile.ZipFile(infilePath) as z:
            for filename in z.namelist():
                if not os.path.isdir(filename):
                    if filename.endswith('.csv'):
                    # read the file
                        with z.open(filename) as f:
                        # reader = csv.reader(filename)

                            #for row in csv.reader(f):
                            for row in f:
                                combinedfile.write(row)
                                '''
                                try:
                                    if any(row):
                                        continue
                                    writer.writerow(row)
                                except:
                                    print "DFDADF"
                                    print row
                                '''
                        f.close()
                                # line = line.replace('\x00', '').split(";")
                                # line = [x.decode('utf8') for x in line]

                                # combinedfile.write(line)
                                #if any(line):
                                    #continue
                                #combinedfile.write(line)

    combinedfile.close()

    Destination384Dict=read_envision_384_csv(combined_file_name)

    #print Destination384Dict
    return Destination384Dict


#combine_csv_dir('/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_3_csv','/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_3_csv/result' )





####parse the input file, generate key value pair of each sequences
def read_384_txt(inFile):
        Infile1 = open(inFile, 'r')
	elisa384PlateCount=0
	Destination384Dict={}
	rowcount =0
	plate96_listA=[] # A1
	plate96_listB=[] # start with A2
	plate96_listC=[] # start with B1
	plate96_listD=[] # B2

        for line in Infile1:
                line = line.strip('\n')
		#print line
                if line.startswith("Plate:"):
			if elisa384PlateCount>0:
				Destination384Dict[Name384]={0:plate96_listA, 1:plate96_listB, 2:plate96_listC, 3:plate96_listD }

			#print str(postive_clone_count_each_plate) + ' clones in plate: ' + plateName + "score >" + str(args.threshold)
                        line=line.split()
			Name384=line[1]
			Destination384Dict[Name384]={}
			rowcount=0
			elisa384PlateCount += 1
			plate96_listA=[] # A1
			plate96_listB=[] # start with A2
			plate96_listC=[] # start with B1
			plate96_listD=[] # B2
		elif not any(c.isalpha() for c in line) and '.'in line:
			rowcount +=1
			line=re.sub('[ \t]+',' ',line)
			line = line.strip().split()
			#print line
			if not '.' in line[0]:
				line.pop(0)
			#print line
			for i in range(len(line)):
				#print line[i]
				#print str(i) + "\t:" + line[i]
				score = float(line[i])
				#try:
				#	score = float(line[i])
				#except:
					#print line[i]
				#	continue

				if (i+1)%2 ==1 and rowcount % 2 ==1:
					plate96_listA.append(score)
				elif (i+1)%2 ==0 and rowcount %2 ==1:
					plate96_listB.append(score)
				elif (i+1)%2 ==1 and rowcount % 2 ==0:
					plate96_listC.append(score)
				elif (i+1)%2 ==0 and rowcount % 2 ==0:
					plate96_listD.append(score)
		else:
			#print "########pass line" + line
			continue

	Destination384Dict[Name384]={0:plate96_listA, 1:plate96_listB, 2:plate96_listC, 3:plate96_listD }
        return Destination384Dict  # platenumaber start with 384 barcode
