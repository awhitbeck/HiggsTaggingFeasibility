from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--strategy", dest="RA2b", default=False,
                  action="store_true",help="use RA2b strategy")
parser.add_option("-m", "--mNLSP", dest="NLSPmass", default=1550,
                  help="mass of the NLSP, can only be 1550, 1000, or 150")
parser.add_option("-l", "--lumiMult", dest="lumiMult", default=1.,
                  help="multiplication factor for luminosity")
parser.add_option("-o", "--outdir", dest="outdir", default="mGluino1600Datacards/",
                  help="output directory")

(options, args) = parser.parse_args()

# =====================
# configuration params
# ---------------------
RA2b = options.RA2b
NLSPmass=int(options.NLSPmass)
outputDir = options.outdir
# =====================

if NLSPmass == 1550 :
    popIndex = [-5,-2,-2]
elif NLSPmass == 1000 :
    popIndex = [-5,-3,-1]
elif NLSPmass == 150 :
    popIndex = [-5,-1,-1]
else : 
    assert 0

if RA2b :
    inputFile = open("mGluino1600yields/bins72.txt")
else :
    inputFile = open("mGluino1600yields/bins18H.txt")

#####################################################

""" yields will be a list (indexed by bin number)
where each element is a dictionary (whos key is the
name of the process) of each process yield."""

processList=[]

binCount = 1

first = True
for line in inputFile : 

    inputs = line[:-1].split()
    #print inputs
    for i in popIndex :
        if first : 
            print "popping out process:",inputs[i]
        inputs.pop(i)
    #print inputs

    if first : 
                
        for p in range( 1 , len(inputs) ) :
            processList.append( inputs[p] )

        first = False
    else : 

        for i in range(len(inputs)) : 
            inputs[i] = str(float(inputs[i])*float(options.lumiMult))
            if inputs[i] == "0" : 
                inputs[i] = "0.000001"
            
        if RA2b :
            outputFile = open("{0}/RA2b_NLSP{2}_bin{1}.txt".format(outputDir,str(binCount),str(NLSPmass)),'w')
        else :
            outputFile = open("{0}/HiggsTagging_NLSP{2}_bin{1}.txt".format(outputDir,str(binCount),str(NLSPmass)),'w')

        outputFile.write("# - - - - - - - - - - - - - - - - - - - \n")
        outputFile.write("# Datacard \n")
        outputFile.write("# - - - - - - - - - - - - - - - - - - - \n")
        outputFile.write("imax 1  number of channels\n")
        outputFile.write("jmax 4  number of backgrounds\n")
        outputFile.write("# - - - - - - - - - - - - - - - - - - - \n")
        outputFile.write("bin {0}\n".format(str(binCount)))
        outputFile.write("observation 1\n")
        outputFile.write("# - - - - - - - - - - - - - - - - - - - \n")
        outputFile.write("bin {0}\n".format(" ".join([str(binCount)]*(len(inputs)-1))))
        outputFile.write("process {0}\n".format(" ".join(processList)))
        outputFile.write("process {0}\n".format(" ".join(map(str,range(len(inputs)-2,-1,-1)))))
        outputFile.write("rate {0}\n".format(" ".join(inputs[1:])))
        outputFile.write("# - - - - - - - - - - - - - - - - - - - \n")
        outputFile.write("ttbarUnc_bin{0} lnN - - - 1.2 - \n".format(str(binCount)))
        outputFile.write("wjetsUnc_bin{0} lnN - 1.2 - - - \n".format(str(binCount)))
        outputFile.write("zjetsUnc_bin{0} lnN 1.2 - - - - \n".format(str(binCount)))
        outputFile.write("QCDUnc_bin{0} lnN - - 1.2 - - \n".format(str(binCount)))
        outputFile.close()
        
        binCount = binCount + 1
