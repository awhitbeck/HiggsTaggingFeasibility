## Description

This repo hosts a simple script for converting a cvs file into datacards to be used with the 
[Higgs Combination tool](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit#How_to_run_the_tool).  
The output a set of datacards that represent one bin for various types of analysis strategies.  These can be found in `mGluion1600/*fb/`.  
The different directories are the same thing, just scale to a specific lumininosity scenario.  Its very likely that his can be done with 
`combine`, but I didn't bother to find out how :(

**Note:**  These notes are based on someone who has some experience with this tool, I am not an expert, and mostly this
is a poor mans quick start.  Don't take anything I say here too seriously and use at your own risk.

## Commands to run

Here are a list of commands that you'll probably be interested in running.  This is only the basics, but if you need to do more advanced stuff 
see the help page `combine --help`, and the twiki page linked above. 

For more things you'll have to do 3 basic things:

- combine several channels (or bins) into one master datacard
- compute the observed or expected 95% confidence level upper limit
- compute the significance of a particular dataset

### Combine datacard (merging all bins)

The script `combineCards.py` takes a list of datacards as arguments and merges them into one grand datacard, which is printed to the standard output.  
To save this output, you should redirect the resulting datacard to the file of your choice.  The inputs can be directed to the script using 
your shell's wildcard:

`combineCards.py myInputs_bin*.txt > myOutput.txt`

### Expected upper limit

With any of your datacards, either a single signal region (or bin) or the combined datacard, you can run a huge number of statistical tests
on the likelihood that is ultimately created from your datacard by `combine`.  One of the more common tests is to compute the expected 
95% C.L. upper limit.  You can use a number of methods for marginalizing the likelihood, see the method option of the help menu. I typically use
the `Asymptotic` method for limits.  To generate an expected limit, you should tell `combine` to use the asimov dataset with the option `-t -1`.

An example of computing the expected UL would be:

`combine -M Asymptotic myDatacard.txt -t -1`

### Expected Significance

For significance, I typically use the `ProfileLikelihood` method.  To get the expected significance assume the signal really exists, you 
should also tell combine that you want to inject signal into your asimov dataset `expectSignal=1`.  An example of this would be

`combine -M ProfileLikelihood myDatacard.txt -t -1 --expectSignal=1`

