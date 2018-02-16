import csv

##### read the barcode table ######
def read_barcode_table(inFile):
    barcodeDir = {}
    if inFile.endswith(".csv"):
        with open(inFile, 'rU') as csvfile:
            readCSV = csv.reader (csvfile, delimiter=',')
            for words in readCSV:
                if words[0].startswith("#"):
                    continue
                #words = line.split()

                if  barcodeDir.get(words[1]):
                    if not words[0] in barcodeDir[words[1]]:
                        barcodeDir[words[1]].append(words[0])
                else:
                    barcodeDir[words[1]] = []
                    barcodeDir[words[1]].append(words[0])

    elif inFile.endswith(".txt"):
            Infile1 = open(inFile, 'r')

            for line in Infile1:
                    if line.startswith("#"):
                        continue
                    words = line.split()
                    if  barcodeDir.get(words[1]):
                        if not words[0] in barcodeDir[words[1]]:
                            barcodeDir[words[1]].append(words[0])
                    else:
                        barcodeDir[words[1]] = []
                        barcodeDir[words[1]].append(words[0])

    else:
        print "Error! The bacode file format should be csv or txt."

    print barcodeDir
    Check96=[len(plate96barcodelist) for barcode384,plate96barcodelist in barcodeDir.iteritems()]
    if len(set(Check96)) >1:
        print "Error in barcode table! Please Revise!"
    else:
        return (barcodeDir,Check96[0])
