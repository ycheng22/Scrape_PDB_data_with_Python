# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:00:52 2020

@author: Yunpeng Cheng

E_mail: ycheng22@hotmail.com

Reference:
"""
import time
tic = time.time()
from multiprocessing.dummy import Pool as ThreadPool
from http.client import IncompleteRead
import sys
#import sub_func #include read_url(), 
import pypdb as pyb #this is a package as pdb API,https://github.com/williamgilpin/pypdb
import urllib.request
import pandas as pd
import numpy as np
import yagmail
import warnings
warnings.filterwarnings("ignore")
#----------------------------------------------------------------------------
opener = urllib.request.build_opener()
opener.addheaders =[('User-agent', 'Mozilla/49.0.2')]
#----------------------------------------------------------------------------
def read_url(id): #read one pdb's content
    url_beg='https://files.rcsb.org/view/'
    url_end='.pdb'
    url=url_beg+id+url_end
    fill_str=' '*20
    arr_store=np.full(17, fill_str)
    arr_store[0]=id    
    try:
        try_open=opener.open(url)
        content = try_open.read().decode('utf-8')
        ct=content.split("\n")
        arr_store[1]=ct[0][10:49].rstrip() #header
        arr_store[2]=ct[0][50:59] #date
        for ln in ct:   
            if ("CRYST1" in ln) & ("REMARK" not in ln): 
                arr_store[3]=ln[6:15].lstrip() #a
                arr_store[4]=ln[15:24].lstrip() #b
                arr_store[5]=ln[24:33].lstrip() #c
                arr_store[6]=ln[33:40].lstrip() #alpha
                arr_store[7]=ln[40:47].lstrip() #beta
                arr_store[8]=ln[47:54].lstrip() #gamma
                arr_store[9]=ln[54:65].strip()  #space group
                continue
            
            if ("RESOLUTION RANGE HIGH (ANGSTROMS)" in ln): #REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) : 2.85          
                arr_store[10]=ln[49:55].rstrip() #reso high
                continue
            if ("RESOLUTION RANGE LOW  (ANGSTROMS)" in ln): 
                arr_store[11]=ln[49:55].rstrip() #reso low
                continue
            if ("SOLVENT CONTENT" in ln): 
                arr_store[12]=ln[38:-20].rstrip() #solvent content
                continue
            if ("COMPND" in ln) & ("CHAIN" in ln):#in .pdb: COMPND   3 CHAIN: A;    
                arr_store[13]=ln[18:-10].replace(';','').rstrip() #chain names
                continue
            if ("PROTEIN ATOMS        " in ln): 
                arr_store[14]=ln[40:-15].rstrip() #number of protein atoms
                continue
            if ("FROM WILSON PLOT" in ln): 
                arr_store[15]=ln[49:-15].rstrip() #
                continue
            if ("MEAN B VALUE" in ln):
                arr_store[16]=ln[49:-15].rstrip() #
                continue           
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass
    except IncompleteRead:
        pass
    else:
        pass
    time.sleep(1)    
    return arr_store
#----------------------------------------------------------------------------
all_ids=pyb.get_all()
index_beg=20000 #5000
index_end=20200 #10000
id_store=all_ids[index_beg:index_end] 
len_pick=len(id_store)
para_arr=np.full((len_pick,18), ' '*20)
pool = ThreadPool(4)
#results = pool.map(read_url, id_store)
writer = pd.ExcelWriter("pdb_info_" + str(index_beg) + "_" + str(index_end-1) + ".xlsx")
index=0
for ele in pool.imap(read_url, id_store):
    para_arr[index,0]=index+index_beg
    para_arr[index,1:]=ele    
    sys.stdout.write("\r scrapping %d / %d" %(index+1, len_pick))
    sys.stdout.flush()
    index=index+1
    if (index % 100 == 0) | (index == len_pick):
        
        df = pd.DataFrame(para_arr,columns=["ID_order","ID","Header",
                        "Date","a","b","c","alpha","beta","gamma",
                        "Space_Group","Reso_High","Reso_Low","Sol_Cont",
                        "Chain","Num_Protein_Atom","B_val_wilson","B_val_overall"])
        df.to_excel(writer, index=False,encoding='utf-8',sheet_name="foundID") 
        writer.save()
        time.sleep(1)
pool.close()
pool.join()
#----------------------------------------------------------------------------
#send remind email to when finished.
receiver = "ycheng22@hotmail.com"
body = "job finished!_"+ str(index_beg) + "_to_" + str(index_end-1) 

yag = yagmail.SMTP(user="ycheng2020@gmail.com", password="15138065260cyp", host='smtp.gmail.com')
yag.send(
    to=receiver,
    subject=body,
    contents=body, 
)
#----------------------------------------------------------------------------
toc = time.time()
print("\n Time elapsed:", toc - tic, "seconds")  
