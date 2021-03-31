# Scrape_PDB_data_with_Python

## Purpose

In my research, I need to filter strucure in [Protein Data Bank](https://www.rcsb.org/) by solvent content, resolution, space group, etc. 

The search option on the website is not good enough for me, so I want filter those structures in my custom criteria.

After reading the book "Ryan Mitchell - Web Scraping with PythonO’Reilly Media (2018)", it's a good chance to utilize this knowledge to fullfil my goal. 

## Files description

`scrap_pdb_improv_thread_mem.py` is the final python code I used.

Because there are 160k+ datas, I need to scrape step by step, the output file looks like: `pdb_info_0_999.xlsx`, `pdb_info_1000_2799.xlsx`.

To free my laptop, I ran the code on cluster, file `job_py.slurm` is used to submit job to cluster. 
