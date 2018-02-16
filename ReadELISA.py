
import re
import csv
import os
import glob
import zipfile
import codecs
import logging
#####
######### iniate new data ########
def initiate_new_plate():
    rowcount =0
    listA=[] # A1
    listB=[] # start with A2
    listC=[] # start with B1
    listD=[] # B2
    return (rowcount,listA,listB,listC,listD)


#read_envision_384_csv('./rawdata/ensingle.csv')
#read_384_csv('Plate2.csv')

######## parse_384row###
def parse_384row(rowlist):
    newlist=[]
    # ignore line 1 2 3 4 5 ... 12
    if '123456789101112' in ''.join(rowlist):
        return []
    tmp_row = [ ele for ele in rowlist if ele ] # select all non empty elements from rowlist
    for i in range(len(tmp_row)):
        try:
            score = float(tmp_row[i])
        except:
            continue
        newlist.append(score)
    if len(newlist)== 24:
        return newlist
    elif len(newlist) == 25:
        newlist.pop(0)
        return newlist
    else:
        # logging.error("The following line is not raw data line")
        # logging.error(rowlist)
        # logging.error(newlist)
        return []


########  Read dry 384 only ###########
def convert_384row_4list(rowlist,rowcount,listA,listB,listC,listD):
    #if rowlist == None:
    #    return
    #if len(rowlist) <24:
    #    return
    for i in range(len(rowlist)):
        try:
            score = float(rowlist[i])
        except:
            continue
        if (i+1)%2 ==1 and rowcount % 2 ==1:
            listA.append(score)
        elif (i+1)%2 ==0 and rowcount %2 ==1:
            listB.append(score)
        elif (i+1)%2 ==1 and rowcount % 2 ==0:
            listC.append(score)
        elif (i+1)%2 ==0 and rowcount % 2 ==0:
            listD.append(score)
    return (listA,listB,listC,listD)

########## combine 4 lists into one dictionary####
def combine_4list_dic(listA,listB,listC,listD):
    combined_dic= {0:listA, 1:listB, 2:listC, 3:listD }
    return combined_dic



########## this can be a single plate data, as well as combined multiple plate data from ENvision###
def read_EnVision_384_csv(inFile):
    elisa384PlateCount=0
    single384Dict={}
    rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD = initiate_new_plate()
    findBarcode = False
    with open(inFile,'rbU') as csvfile:
        readCSV = csv.reader((x.replace('\0','') for x in csvfile))
        for row in readCSV:
            if len(row) == 0: # ignore empty line
                continue

            if findBarcode == True:
                if elisa384PlateCount >= 1:
                    single384Dict[barcode_name] = combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
                barcode_name= row[barcode_pos]
                findBarcode = False
                rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD = initiate_new_plate()
                elisa384PlateCount += 1
            elif 'Barcode' in row:
                findBarcode = True
                barcode_pos = row.index('Barcode')
            elif len(row) >= 24: # find the real data
                row = parse_384row(row)
                rowcount += 1
                plate96_listA,plate96_listB,plate96_listC,plate96_listD = convert_384row_4list(row,rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD)

    logging.debug(elisa384PlateCount)
    if elisa384PlateCount > 0 :
        single384Dict[barcode_name]=combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
    else:
        logging.debug("Warning! No ELISA data was found!")
    '''
    for key in single384Dict:
        print key
        print single384Dict[barcode_name][0]
        print single384Dict[barcode_name][1]
        print single384Dict[barcode_name][2]
        print single384Dict[barcode_name][3]
    print single384Dict
    '''
    return single384Dict



########## this can be a single plate data, as well as combined multiple plate data from MD (MolecularDevice)###
def read_MD384_csv(inFile):
    elisa384PlateCount=0
    Single384Dict={}
    barcode_name=''
    rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD = initiate_new_plate()
    findBarcode = False
    findTemp = False
    with open(inFile,'rbU') as csvfile:
        readCSV = csv.reader(x.replace('\0','') for x in csvfile)
        for row in readCSV:
            if not row: # ignore empty line
                continue

            if row[0].startswith('Plate:'):
                if elisa384PlateCount >=1:
                    #print "??????????????? elisa"
                    Single384Dict[barcode_name] = combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
                rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD = initiate_new_plate()
                barcode_name = row[1]
                elisa384PlateCount += 1

            elif len(row) >=24: # find the real data
                # print row
                row = parse_384row(row)
                rowcount +=1
                plate96_listA,plate96_listB,plate96_listC,plate96_listD = convert_384row_4list(row,rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD)

        logging.debug(elisa384PlateCount)
        if elisa384PlateCount > 0 :
            Single384Dict[barcode_name]=combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
        else:
            logging.debug("Warning! No ELISA data was found!")
    # print Single384Dict
    return Single384Dict  # platenumaber start with 384 barcode



########## this can be a single plate data, as well as combined multiple plate data from MD (MolecularDevice)###
def read_PHERAstar_384_csv(inFile):
    print "Runnning read_PHERASTAR"
    elisa384PlateCount=0
    Single384Dict={}
    barcode_name=''
    rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD = initiate_new_plate()
    findBarcode = False
    findTemp = False
    with open(inFile,'rbU') as csvfile:
        readCSV = csv.reader(x.replace('\0','') for x in csvfile)
        for row in readCSV:
            #print row
            if not row: # ignore empty line
                continue

            if row[0].startswith('Date:'):
                #print "row[0]: " + row[0]
                if elisa384PlateCount >=1:
                    #print "??????????????? elisa"
                    Single384Dict[barcode_name] = combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
                (rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD) = initiate_new_plate()
                #barcode_name = row[1]
                elisa384PlateCount += 1

            elif row[0].startswith('<'):
                temp= re.findall(r'^<(.*)>', row[0])
                #temp=row[0].split()
                if temp:
                    barcode_name= temp[0]
                    print barcode_name

            elif len(row) >=24: # find the real data
                row = parse_384row(row)
                rowcount +=1
                plate96_listA,plate96_listB,plate96_listC,plate96_listD = convert_384row_4list(row,rowcount,plate96_listA,plate96_listB,plate96_listC,plate96_listD)


        logging.debug(elisa384PlateCount)
        if elisa384PlateCount > 0 :
            Single384Dict[barcode_name]=combine_4list_dic(plate96_listA,plate96_listB,plate96_listC, plate96_listD )
        else:
            logging.debug("Warning! No ELISA data was found!")
    #print Single384Dict
    return Single384Dict  # platenumaber start with 384 barcode


###### read all csv files in the file
def combine_csv_dir(infilePath,outfilePath):
    print "running combine_csv_dir"
    combined_file_name= os.path.join(outfilePath,'combined.csv')
    combinedfile = open(combined_file_name, 'wb')
    writer = csv.writer(combinedfile)

    Destination384Dict={}

    if infilePath.endswith(".zip"):
        print "find zip"
        with zipfile.ZipFile(infilePath) as z:
            for filename in z.namelist():
                if not os.path.isdir(filename):
                    if filename.endswith('.csv'):
                        #print filename
                    # read the file
                        with z.open(filename) as f:
                            for row in f:
                                #print row
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
                        combinedfile.write('\n')
    elif infilePath.endswith(".csv"):
        with open(infilePath) as f:
            for row in f:
                combinedfile.write(row)
    combinedfile.close()


    detector = identify_detector_type(combined_file_name)
    if detector == "EnVision":
        Destination384Dict = read_EnVision_384_csv(combined_file_name)
    elif detector == "MolecularDevice":
        Destination384Dict = read_MD384_csv(combined_file_name)
    elif detector == "PHERAstar":
        Destination384Dict = read_PHERAstar_384_csv(combined_file_name)

    #print Destination384Dict
    return Destination384Dict



##########
'''
def check_data_line(indict):
    if len(indict) < 23:
        return False
    count_continue_dot=0
    for item in indict:
        if '.' in item:
            count_continue_dot +=0
    return
'''


#######
def print_dict(inputdict):
    print inputdict.keys()
    print len(inputdict.keys())


    '''
    for k, v in inputdict.iteritems():
        print k

        for k1, v1 in v.iteritems():
            print k1
            print v1
    '''

########  identify reader type ######
def identify_detector_type (inputfile):
    combinedfile = open(inputfile, 'r')
    first = combinedfile.readline()
    #print first
    if first.startswith("Plate information"):
        logging.info("#### The detector is EnVision.    ####")
        return "EnVision"
    elif first.startswith("##BLOCKS"):
        logging.info("#### The detector is MolecularDevice.   ####")
        return "MolecularDevice"
    elif first.startswith('Testname'):
        logging.info("#### The detector is PHERAstar.   ####")
        return "PHERAstar"
    else:
        logging.info("#### Couldn't identify the Reader type.   ####")
        print "Couldn't identify the Reader type"


#detector = identify_detector_type ("./result/combined.csv")
#print detector
#detector = identify_detector_type ("./result/MD_combined.csv")
#print detector
#detector =identify_detector_type ("./result/star_combined.csv")
#print detector


#################### Main ###########################
a= combine_csv_dir('./rawdata/ensingle.csv', './rawdata/') #read_MD384_csv('./rawdata/MD.csv')

#a= combine_csv_dir('/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/rawdata/TIM1_group62', '/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/result/')
#a= read_PHERAstar_384_csv('/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/rawdata/DES23.csv')
#print_dict(a)
