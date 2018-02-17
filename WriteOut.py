# write output files accoriding to the ELSIA setup
import MatrixConversion
import os
###############################
def write_1antigen_4Ab(Dict384,barcodeDir,threshold, outfileNamePrefix):
	OutfileName1= outfileNamePrefix+"/1antigen4Ab_all.csv"
	Outfile1= open(OutfileName1,"w+")
	Outfile1.write('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID , OD\n')
	OutfileName2= outfileNamePrefix+"/1antigen4Ab_positivelist.csv"
	Outfile2=open(OutfileName2,'w+')
	Outfile2.write('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID , OD \n')
	positiveRatio_Dict={}

	for name384 in sorted(Dict384.iterkeys()):
	#for name384,plates96 in Dict384.iteritems():
		for j in range(4):
			for i in range(96):
				source96wellID= MatrixConversion.humanize(i+1)
				output= name384+','+barcodeDir[name384][j]+'_'+source96wellID+ ','+ barcodeDir[name384][j]+','+source96wellID +','+ str(Dict384[name384][j][i])+'\n'
				Outfile1.write (output)

				if Dict384[name384][j][i] >=threshold:
					Outfile2.write (output)
					positiveRatio_Dict[barcodeDir[name384][j]+'_'+source96wellID] = Dict384[name384][j][i]
        print "The 1antigen 4ab data have been assembled in list:"  + OutfileName1
        print "The 1antigen 4ab data (selected based on threshold ratio) have been assembled in list:" + OutfileName2
        write_selected_into96(positiveRatio_Dict, outfileNamePrefix)
        #print positiveRatio_Dict

	Outfile1.close()
	Outfile2.close()

	return

###########################

def write_4antigen_1Ab(Dict384,barcodeDir,background_pos, sample_pos, ratio_threshold, outfileNamePrefix):
	OutfileName1 = outfileNamePrefix+"/4antigen1Ab_all.csv"
	Outfile1 = open(OutfileName1, 'w+')
	OutfileName2 = outfileNamePrefix+"/4antigen1Ab_positivelist.csv"
	Outfile2 = open(OutfileName2, 'w+')
	positiveRatio_Dict={}

	Outfile1.write ('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID ,1st Antigen,2nd Antigen,3rd Antigen,4th Antigen , sample'+str(sample_pos) + '/background'+str(background_pos)+'\n')
	Outfile2.write ('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID ,1st Antigen,2nd Antigen,3rd Antigen,4th Antigen , sample'+str(sample_pos) + '/background'+str(background_pos)+'\n')

	for name384 in sorted(Dict384.iterkeys()):
		for i in range(96):
			ratio = Dict384[name384][sample_pos-1][i]/Dict384[name384][background_pos-1][i]
			source96wellID= MatrixConversion.humanize(i+1)
			output= name384+','+barcodeDir[name384][0]+'_'+source96wellID+ ','+ barcodeDir[name384][0]+','+source96wellID +','+ str(Dict384[name384][0][i])+','+str(Dict384[name384][1][i]) +','+str(Dict384[name384][2][i]) +','+str(Dict384[name384][3][i]) +','+ str(ratio)+'\n'
			Outfile1.write (output)

			if ratio >=ratio_threshold:
				positiveRatio_Dict[barcodeDir[name384][0]+'_'+source96wellID] = ratio
				Outfile2.write (output)
	print "The 4antigen 1ab data have been assembled in list:"  + OutfileName1
	print "The 4antigen 1ab data (selected based on threshold ratio) have been assembled in list:" + OutfileName2
	write_selected_into96(positiveRatio_Dict, outfileNamePrefix)
	#print positiveRatio_Dict
	return

#############################################################################################
def write_2antigen_2Ab(Dict384,barcodeDir,background_pos, sample_pos, ratio_threshold, outfileNamePrefix):
	if sample_pos >2 or background_pos >2:
		print "Error! background position or sample position should be either 1 or 2."
		return

	OutfileName1 = os.path.join(outfileNamePrefix,"2antigen2Ab_all.csv")
	Outfile1 = open(OutfileName1, 'w+')
	OutfileName2 = os.path.join(outfileNamePrefix,"2antigen2Ab_positivelist.csv")
	Outfile2 = open(OutfileName2, 'w+')
	positiveRatio_Dict={}
	Outfile1.write ('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID ,1st Antigen,2nd Antigen, sample'+str(sample_pos) + '/background'+str(background_pos)+'\n')
	Outfile2.write ('Destination(384) barcode , Alias, Source(96) barcode, Source(96) wellID ,1st Antigen,2nd Antigen, sample'+str(sample_pos) + '/background'+str(background_pos)+'\n')
	for name384 in sorted(Dict384.iterkeys()):
		j=0
		while (j <4):
			for i in range(96):
				source96wellID= MatrixConversion.humanize(i+1)
				if j<2:
					ratio = Dict384[name384][sample_pos-1][i]/Dict384[name384][background_pos-1][i]
					aliasID= barcodeDir[name384][0]+'_'+source96wellID
					barcode96 = barcodeDir[name384][0]
				else:
					ratio = Dict384[name384][sample_pos+1][i]/Dict384[name384][background_pos+1][i]
					aliasID= barcodeDir[name384][1]+'_'+source96wellID
					barcode96 = barcodeDir[name384][1]
				output= name384+','+aliasID+ ','+ barcode96+','+source96wellID +','+ str(Dict384[name384][j][i])+','+str(Dict384[name384][j+1][i]) +','+ str(ratio)+'\n'
				Outfile1.write (output)

				if ratio >=ratio_threshold:
					positiveRatio_Dict[aliasID] = ratio
					Outfile2.write (output)

			j =j+2
	Outfile1.close()
	Outfile2.close()
	print "The 4antigen 1ab data have been assembled in list:%s"  % OutfileName1
	print "The 4antigen 1ab data (selected based on threshold ratio) have been assembled in list:" + OutfileName2
	write_selected_into96(positiveRatio_Dict, outfileNamePrefix)
	return


#####################
def write_selected_into96(Dict,outfileNamePrefix):
	OutfileName = outfileNamePrefix +'/pos_in96format.csv'
	Outfile = open (OutfileName, 'w+')
	count =0
	keys = Dict.keys()
	keys.sort()
	for key in keys:

		if count % 96 ==0:
			Outfile.write("\n\n,1,2,3,4,5,6,7,8,9,10,11,12")
			count =0
		if count% 12 ==0:
			Outfile.write ("\n"+ chr((count/12)+65)+ ',')
		Outfile.write(key+',')
		#Outfile.write(str(value)+',')
		count +=1

	print "positive clones have been reformated into 96well plate: " + OutfileName
        return
