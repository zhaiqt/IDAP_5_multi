#!/usr/bin/env python

import argparse
import re
import WriteOut
import ReadBarcode
import ReadELISA
import zipfile
import logging

#######################
#python IDAP384screen.py -i /Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_star/rawdata/ensingle.csv.zip -c /Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_star/rawdata/barcode_Table.csv -o /Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_star/result
parser = argparse.ArgumentParser( prog='CherryPicking',description="ELISA plate cheery picking", epilog='python CherryPick384.py -i inputfile.txt -d detector_type -c barcodefile.txt -s threshold -a samplePos -b backgroundPos -r ratio_threshold -o outputpath')
parser.add_argument('-c','--barcode', help="Input bacode table file .txt", default ="/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/rawdata/plates1to30barcodes.csv")
parser.add_argument ('-i','--inputpath',help='Input directory', default="/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/rawdata/WHVFCIGGPLATES1TO30.zip")
#parser.add_argument ('-d','--detector', help ='Reader type: MolecularDevice or EnVision or PHERAstar', type = str, default ='MolecularDevice')
parser.add_argument('-s','--threshold', help="the cutof for the elisa", type= float,  default= '0.6')
parser.add_argument('-r','--ratio_threshold', help="the ratio for the elisa", type=float, default='3')
parser.add_argument('-b','--backgroundPos', help='1 or 2 or 3 or 4', type=int, default='4')
parser.add_argument('-a','--samplePos', help='1 or 2 or 3 or 4', type=int, default='2')
parser.add_argument('-o', '--outputpath',help='outputpath for output',default='/Users/zhaiqi1/Documents/Novartis/my_code/ToolBox/IDAP384screen/IDAP_5_multi/result')
parser.print_help()
args=parser.parse_args()
print args

log_file = args.outputpath+'/runlog.txt'
log_level = logging.DEBUG
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s %(message)s')

raw384dir=ReadELISA.combine_csv_dir(args.inputpath, args.outputpath)


BarcodeDir,Number96per384 = ReadBarcode.read_barcode_table (args.barcode)  # read barcode table
# example of BarcodeDir   {'Destinationbarcode': ['souceplate1', 'souceplate2', 'sourceplate3', 'sourceplate4']}
print "print raw384 directory key:"
print raw384dir.keys()

print "Keys of barcode"
print BarcodeDir.keys()
tmp=''
logging.info ("Plate names extracted from the raw data file:")
k=''
for k in raw384dir.keys():
    tmp = tmp + " " + k
logging.info(k)

logging.info ("Plate names extracted from barcode table:")
tmp=''
for k in BarcodeDir.keys():
    tmp = tmp + " " + k
logging.info(k)


logging.info('The are '+ str(len(raw384dir.keys())) +' 384-well ELISA plates.\n')
logging.info('The are '+ str(len(BarcodeDir.keys())) +' destination plates.\n')
if set(raw384dir.keys()) <= set(BarcodeDir.keys()):
    if Number96per384 ==4:  # which is equal to "A" or '1antigen' or '4antibody'
        print "**Based on Barcode table file: The experiment setup is 1antigen X 4Ab. So the samplePos,the backgroundpos and ratio shreshold are ignored.\n"
        logging.info('The experiment setup is 1antigen X 4Ab. So the samplePos,the backgroundpos and ratio shreshold are ignored.\n')
        WriteOut.write_1antigen_4Ab (raw384dir, BarcodeDir,args.threshold,args.outputpath )

    elif Number96per384 == 1:   # layoutMode  is  'B' or '4antigen' or '1antibody'
        print "**Based on Barcode table file: The experiment setup is 4antigen X 1Ab.\n"
        logging.info('The experiment setup is 4antigen X 1Ab.\n')
        WriteOut.write_4antigen_1Ab(raw384dir,BarcodeDir,args.backgroundPos, args.samplePos, args.ratio_threshold,args.outputpath )

    elif Number96per384 == 2: #layoutMode is  'C' or '2antigen' or '2antibody''
        print "**Based on Barcode table file:: The experiment setup is 2antigen X 2Ab.\n"
        logging.info('The experiment setup is 2antigen X 2Ab.\n')
        WriteOut.write_2antigen_2Ab(raw384dir,BarcodeDir,args.backgroundPos, args.samplePos, args.ratio_threshold,args.outputpath )

    else:
    	#print "Error in layoutMode! Check " + args.barcode +"!"
        logging.info("Error in layoutMode! Check barcode tabe.\n")
else:
    logging.info('Error: The ELISA barcodes do not match the barcode table.\n')
