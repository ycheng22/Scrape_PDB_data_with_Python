# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:11:09 2020

@author: Yunpeng Cheng

E_mail: ycheng22@hotmail.com

Reference:
"""
import time
tic = time.time()
import sys
import pypdb as pyb #this is a package as pdb API,https://github.com/williamgilpin/pypdb
import urllib.request
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
#----------------------------------------------------------------------------
opener = urllib.request.build_opener()
opener.addheaders =[('User-agent', 'Mozilla/49.0.2')]
all_ids=pyb.get_all()
index_beg=0
index_end=101
id_store=all_ids[index_beg:index_end] ###choose partial entries when debugging
len_id=len(id_store)
#----------------------------------------------------------------------------
fill_str=' '*20
id_not_fd_HTTPError=[]
id_not_fd_URLError=[]
id_fd=np.full(len_id, fill_str)
header=np.full(len_id, fill_str)
date=np.full(len_id, fill_str)
chain_fd=np.full(len_id, fill_str)
reso_high=np.full(len_id, fill_str)
reso_low=np.full(len_id, fill_str)
num_protein_atom=np.full(len_id, fill_str)
B_val_wilson=np.full(len_id, fill_str)
B_val_overall=np.full(len_id, fill_str)
sol_cont=np.full(len_id, fill_str)
aa=np.full(len_id, fill_str)
bb=np.full(len_id, fill_str)
cc=np.full(len_id, fill_str)
alpha=np.full(len_id, fill_str)
beta=np.full(len_id, fill_str)
gamma=np.full(len_id, fill_str)
space_gp=np.full(len_id, fill_str)
#----------------------------------------------------------------------------
url_beg='https://files.rcsb.org/view/'
url_end='.pdb'
for index, id in enumerate(id_store):
    sys.stdout.write("\r scrapping %d / %d" %(index+1, len_id))
    sys.stdout.flush()
    #print("scrapping " + str(index) + "th id of " + str(len_id-1) + " IDs")
    url=url_beg+id+url_end
    try:
        try_open=opener.open(url)
        id_fd[index]=id
        content = try_open.read().decode('utf-8')
        ct=content.split("\n")
        header[index]=ct[0][10:49].rstrip() #what kind of protein
        date[index]=ct[0][50:59]
        for ln in ct:       
            if ("COMPND" in ln) & ("CHAIN" in ln):#in .pdb: COMPND   3 CHAIN: A;    
                chain_fd[index]=ln[18:-10].replace(';','').rstrip()
                continue
            if ("RESOLUTION RANGE HIGH (ANGSTROMS)" in ln): #REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) : 2.85          
                reso_high[index]=ln[49:55].rstrip()
                continue
            if ("RESOLUTION RANGE LOW  (ANGSTROMS)" in ln): 
                reso_low[index]=ln[49:55].rstrip()
                continue
            if ("PROTEIN ATOMS" in ln): 
                num_protein_atom[index]=ln[40:-15].rstrip()
                continue
            if ("FROM WILSON PLOT" in ln): 
                B_val_wilson[index]=ln[49:-15].rstrip()
                continue
            if ("MEAN B VALUE" in ln):
                B_val_overall[index]=ln[49:-15].rstrip()
                continue
            if ("SOLVENT CONTENT" in ln): 
                sol_cont[index]=ln[38:-20].rstrip()
                continue
            if ("CRYST1" in ln) & ("REMARK" not in ln): 
                aa[index]=ln[6:15].lstrip()
                bb[index]=ln[15:24].lstrip()
                cc[index]=ln[24:33].lstrip()
                alpha[index]=ln[33:40].lstrip()
                beta[index]=ln[40:47].lstrip()
                gamma[index]=ln[47:54].lstrip()
                space_gp[index]=ln[54:65].strip() 
                continue
    except urllib.error.HTTPError:
        id_not_fd_HTTPError.append(id)
        #print('HTTPError')
    except urllib.error.URLError:
        id_not_fd_URLError.append(id)
        #print('URLError')
    time.sleep(0.5)
    
    if (index % 100 == 0) | (index == len_id-1):  #save the scrapped data every 50 time, or the last one
        df = pd.DataFrame()
        df["ID"] = id_fd
        df["Header"] = header
        df["a"] = aa
        df["b"] = bb
        df["c"] = cc
        df["alpha"] = alpha
        df["beta"] = beta
        df["gamma"] = gamma
        df["Space_Group"] = space_gp
        df["Reso High"] = reso_high
        df["Reso Low"] = reso_low
        df["Sol_Cont"] = sol_cont
        df["Chain"] = chain_fd
        df["Num_Protein_Atom"] = num_protein_atom
        df["B_val_wilson"] = B_val_wilson
        df["B_val_overall"] = B_val_overall
        df["Date"] = date
        writer = pd.ExcelWriter("pdb_info_" + str(index_beg+1) + "_" + str(index_end) + ".xlsx")
        try:
            df.to_excel(writer, index=False,encoding='utf-8',sheet_name='foundID')                
        except:
            print("cannot write to file")
        if id_not_fd_HTTPError:
            df_HTTPError=pd.DataFrame(id_not_fd_HTTPError)
            df_HTTPError.to_excel(writer, index=False,encoding='utf-8',sheet_name='HTTPErrorID')
        if id_not_fd_URLError:
            df_URLError=pd.DataFrame(id_not_fd_URLError)
            df_HTTPError.to_excel(writer, index=False,encoding='utf-8',sheet_name='URLErrorID')        
        writer.save()
        time.sleep(1)

toc = time.time()
print("\n Time elapsed:", toc - tic, "seconds")  