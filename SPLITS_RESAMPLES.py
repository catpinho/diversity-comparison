import os
import random
def readfasta(ficheiro):
    fich=open(ficheiro,"r")
    linhas=fich.readlines()
    tudo="".join(linhas)
    fich.close()
    split=tudo.split(">")[1:]
    seqs=[]
    for i in split:
        seq=[]
        a=i.split("\n")
        seq.append(a[0])
        b="".join(a[1:])
        b=b.upper()
        seq.append(b)
        seqs.append(seq)
    return seqs

filelist=raw_input("Please enter the name of the file containing the list of alignments: ")
grouppos=int(raw_input("Please enter the position of the group identifier in the sequence name: ")) -1
files=[]
f=file(filelist,"r")
fr=f.read()
fs=fr.split("\n")
for fic in fs:
    if fic not in [""," ","  ","\t","\n","\t\t"]:
        files.append(fic)
groups=[]
for gene in files:
    a=readfasta(gene)
    for seq in a:
        gr=seq[0].split("_")[grouppos]
        if gr not in groups:
            if gr not in [""," ","\n","  "]:
                groups.append(gr)
N=int(raw_input("How many resamples to take? "))
for gene2 in files:
    numb=[]
    a2=readfasta(gene2)
    if ".fasta" in gene2:
        fas=".fasta"
    elif ".FASTA" in gene2:
        fas=".FASTA"
    else:
        if ".FAS" in gene2:
            fas=".FAS"
        else:
            fas=".fas"
    os.system("ren "+gene2+" "+gene2.split(fas)[0]+".fas")
    for group in groups:
        nu=0
        o=file(group+"_"+gene2.split(fas)[0]+".fas","w")
        for seq2 in a2:
            gr2=seq2[0].split("_")[grouppos]
            if gr2==str(group):
                o.write(">"+seq2[0]+"\n"+seq2[1]+"\n")
                nu+=1
        o.close()
        numb.append(nu)
    numb.sort()
    k=numb[0]
    ind=0
    #the default is to consider sample sizes equal or higher than 2. If you think 2 is too low you can replace the 2 in the line below by the number of your choice.
    while k<2:
        if ind+1<len(numb):
            ind+=1
            k=numb[ind]
        else:
            k=1000000000000000
    print "s in "+gene2+" is: "+str(k)
    #if you want to specify a fixed resample size for all loci, remove the # from the line below and replace "define_here" by the number of your choice 
    #k=define_here
    for group in groups:
        f=readfasta(group+"_"+gene2.split(fas)[0]+".fas")
        if len(f)>k:
            for i in range(N):
                o2=file(str(group)+"_"+"r"+str(i+1)+"_"+gene2.split(fas)[0]+".fas","w")
                s=random.sample(f,k)
                for seq in s:
                    o2.write(">"+seq[0]+"\n"+seq[1]+"\n")
                o2.close()
        if len(f)==0:
            os.system("del "+group+"_"+gene2.split(fas)[0]+".fas")
