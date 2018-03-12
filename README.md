# diversity-comparison
Pipeline for comparing diversity between localities with different sample sizes

This tutorial explains how to calculate diversity measures for sequence data taking into account different sample sizes across populations. The idea is to estimate the diversity measures for a population if you had sampled only s gene copies (s being the smallest sample size across populations), neutralizing the effect of differential sample sizes in diversity measures and allowing direct comparisons among populations. In order to do this, this procedure will produce N subsets of s gene copies per population and take the average of diversity measures across the N replicates. s is by default higher than 1, which means that groups with sizes 0 or 1 are not taken into account*. Groups of size s are not resampled.
Note that the smallest sample size per locus will be used, meaning that different sizes will be selected depending on the loci**. 

There are three steps to calculate these measures:

1.	Use the script called SPLITS_RESAMPLES.py to generate data files.

2.	Use DNAsp (http://www.ub.edu/dnasp/) to calculate diversity measures in batch mode.

3.	Use the script called CALCULATES_MEANS.py to take the output of DNAsp, choose which diversity measures you want to consider and calculate the mean across resamples for each population.

Here is how this goes step by step:

0.	INSTALL PYTHON


0.1 Download python from

http://www.python.org/download

All my scripts are written using Python 2.X (which is still updated and that I continue to use so that the old scripts keep working) and not Python 3, so please install the latest 2.X version.

0.2	Install python by following the instructions for your OS

0.3	Basics on how to run a script:
Open the script with the IDLE editor which is installed along with Python by choosing the “edit with IDLE” option that appears when you right click on the script, edit whatever requires editing (for these particular scripts, most likely nothing) and press F5. 


1.	SPLITS_RESAMPLES

SPLITS_RESAMPLES.py splits each alignment (in fasta format) in multiple files so that each file will contain info of only one of the groups or populations you are considering. These files are produced because they may be useful to calculate uncorrected diversity measures per group. The second part takes these partial datasets and the smallest sample size (except for sample sizes of 0 or 1) across populations per locus (s) and generates a number N of files, each containing a subset of s sequences per population. This generates a huge amount of files (sorry!) that can be analysed together in batch mode in DNAsp. 

1.1	Prepare the alignments in fasta format (one per locus, with all the groups or populations together). 
Each of the sequences in each fasta file needs to mention the group/population to which it belongs, separated by “_”. It doesn’t matter if the group comes before the sequence name or after, or in the middle – you will be asked that too. Therefore you can sequentially use the same file with different groups (but not at the same time – that would be very confusing!). Note that the group/sequence description cannot contain any “_” itself.
Example of sequence names you can include:
>Cl1_A1_P
>Cl1_B1_P
>Cl2_C1_P
>Cl3_D1_S

Here I was thinking of three sequences from Portugal (P) and one from Spain (S), belonging to three different clades (Cl1, Cl2, Cl3) – but you can use whatever and how many names you want.
You just need to make sure that the groups are defined in the same way for all the sequences in all the alignments. 

1.2	Prepare a file containing the names of the alignments (one per locus) which will be included in the analysis. Each name should be in a different line.
Example:
Nd4_podarcis.fas
Cytb_corrected.fas

NOTE: If you have a gene called r1, r2 or something like that (r plus a number) please call your alignment something else or this will create confusion with the replicates downstream (also coded r1, r2, etc.)

1.3	Save all the files (alignments, list of fastas and script) in the same folder.

1.4	Run the script.

1.5	You will be asked to write the name of the fasta list. Please include the extension.

1.6	The script will ask you which part of the sequences’ names is the partition you want to consider (you could try to compare clades or geographic regions here, for example). In the example I gave you could pick 1 (Cl1, Cl2, Cl3), 2 (A1, B1, C1, D1) or 3 (P,S) here (although if you chose 2 you would be analyzing as many groups as there are sequences).

1.7	You will then be asked how many times you want to take samples from your data (N). I usually take 100 but keep in mind that when sample sizes are small these 100 samples will not be all different from one another (there is a limited number of possible arrangements). I don’t think there is a problem in taking 100 samples even if some are repeated – the average will not be affected by this fact.

This script generates two sets of files:
-	One named X_FILENAME.fas, in which X will be the name of the group. In theory you should have as many files as genes x groups (e.g. 3 genes, 5 groups mean 15 files), but because some files may be empty due to missing data they will be deleted (otherwise DNAsp would crash, I think!). These are the full data set divided by group.
-	Another called X_rY_FILENAME.fas (in which X is the group and Y the number of the replicate, 1≤Y≤N). These are the resampled data (partial data sets of size s).

NOTES: 
I have not added the following features as optional to simplify the script, but you might want to try them. You will have to change the code yourself, but I have added comments that will help you do this.
*Use a smallest sample size (s) higher than 2. Replace the 2 in “while k<2” (line 47) by the number of your choice. 
**Use the same s for all loci. Choose the value you want and replace the expression “define_here” in line 55 by that value. Remove the # from that line.


2.	DNAsp

2.1	Open DNAsp (to write this protocol I used version 5.10.01, so things are probably different now).
2.2	Select File>Open Multi Data Files (Batch Mode)
2.3	Select “add an entire folder” and choose the folder where the files are.
2.4	Click the box to select the whole folder.
2.5	Select the desired name and location of the output and error files.
2.6	Make the adjustments according to your needs.
2.7	Press run.

3.	CALCULATES_MEANS.py 

3.1	Place the script in the same folder of DNAsp output and run it.
3.2	You will be prompted to write the input (DNAsp batch output) and output file names.
3.3	If you open the output in excel, you should have a table with the data: first the result for the full data set (independently of the group). Then the actual results for each group/population, followed by the results of the means in a separate line.
Groups with a sample size of 0 will not appear in this table since DNAsp does not take them into account. Groups with sample size s will have a “-“ instead of a value.
Currently only part of the statistics present in the DNAsp output appears in the final output. If you want to add or remove columns to the table, you can edit the script and change the number of the columns included in line 27. Note that python starts counting from 0 (the first column is 0, the second is 1, etc.).

