fich=file(raw_input("Please write the name of the DNAsp batch output: "),"r")
o=file(raw_input("Desired output name: "),"w")
linhas1=fich.read()
linhas2=linhas1.replace(",",".")
linhas3=linhas2.split("\n")
linhas=[]
groups=[]
genes=[]
for l in linhas3[1:]:
    if l!="":
        if "by DnaSP" not in l:
            if "Error file" not in l:
                if "Calculated using" not in l:
                    linhas.append(l)
                    u=l.split("\t")[0].split(".fas")[0].split("_")
                    if u[1][0]=="r":
                        try:
                            x=int(u[1][1:])
                        except ValueError:
                            x="string"
                        if type(x)==int:
                            a="_".join(u[2:])
                            if a not in genes:
                                genes.append(a)
                            if u[0] not in groups:
                                groups.append(u[0])
#add or remove columns below
cols=[4,5,6,7,8,9,10,12,14,15,16]
o.write("Data\tGroup")
for c in cols:
    o.write("\t"+linhas3[0].split("\t")[c])
o.write("\n")
for gene in genes:
    for linha in linhas:
        li=linha.split("\t")
        u=li[0].split(".fas")[0]
        if u==gene:
            o.write(u+"\tTotal dataset")
            for c in cols:
                o.write("\t"+li[c])
            o.write("\n")
    for group in groups:
        res=[]
        for linha in linhas:
            t=linha.split("\t")
            nomesp=t[0].split("_")
            if nomesp[0]==str(group):
                cod="full"
                if nomesp[1][0]=="r":
                    try:
                        x2=int(nomesp[1][1:])
                    except ValueError:
                        x2="string"
                    if type(x2)==int:
                        cod="resamp"
                        if "_".join(nomesp[2:]).split(".fas")[0]==gene:
                            resrep=[]
                            for c in cols:
                                bo=t[c]
                                if bo in ["n.a.","n.d."]:
                                    bo="0"
                                resrep.append(bo)
                            res.append(resrep)
                if cod=="full":
                    if "_".join(nomesp[1:]).split(".fas")[0]==gene:
                        o.write(gene+"\t"+str(group))
                        for c in cols:
                            o.write("\t"+t[c]) 
                        o.write("\n")
        o.write("\t")
        if len(res)>0:
            for stat in range(len(res[0])):
                x=[]
                for i in range(len(res)):

                    if res[i][stat]!="n.a.":
                        x.append(float(res[i][stat]))
                if len(x)!=0:
                    o.write("\t"+str(sum(x)*1.0/len(x)))
                else:
                    o.write("\t(n.a.)")
            o.write("\n")
        else:
            for c in cols:
                o.write("\t-")
            o.write ("\n")
        o.write("\n")
o.close()
            
        
    
