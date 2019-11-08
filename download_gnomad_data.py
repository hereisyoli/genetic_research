#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import pandas as pd
import numpy as np


# In[14]:


# type the gene's name in the gene_id_list here!!
gene_id_list = [
    "OR52M1", "OR51B5", "OR52N4", "OR11H1", "OR4K15", "OR6S1", "OR5AP2", "OR5H1", "OR13C2", "OR2K2", "OR8G5", "OR1L3", "OR2T27"]
saved_list = []


def fetch(jsondata, url="https://gnomad.broadinstitute.org/api"):
    # The server gives a generic error message if the content type isn't
    # explicitly set
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=jsondata, headers=headers)
    json = response.json()
    if "errors" in json:
        raise Exception(json["errors"])
    return json


def get_variant_list(gene_id, dataset="gnomad_r2_1"):
    # Note that this is GraphQL, not JSON.
    fmt_graphql = """
    {
        gene(gene_name: "%s") {
            variants(dataset: %s) {
                consequence
                pos
                rsid
                ref
                alt
                flags
                lof
                consequence_in_canonical_transcript
                gene_symbol
                chrom
                hgvsc
                reference_genome
                exome {
                  ac
                  ac_hemi
                  ac_hom
                  an
                  af
                }  
                lof_filter
                genome {
                  ac
                  ac_hemi
                  ac_hom
                  an
                  af
                }
                lof_flags
                hgvsc
                hgvsp
                reference_genome
                variant_id: variantId
            }
        }
      }
    """
    # This part will be JSON encoded, but with the GraphQL part left as a
    # glob of text.
    req_variantlist = {
        "query": fmt_graphql % (gene_id, dataset),
        "variables": {}
    }
    response = fetch(req_variantlist)
    return response["data"]["gene"]["variants"]


# add the gene_id at the last column
def make_df(gene_id):
    li = get_variant_list(gene_id)
    df = pd.DataFrame(li)
    return df


# get_header
header = [
    'Name',
    'Chromosome',
    'Position',
    'rsID',
    'Reference',
    'Alternate',
    'Protein Consequence',
    'Transcript Consequence',
    'Annotation',
    'Flags',
    'Allele Count',
    'Allele Number',
    'Allele Frequency',
    'Homozygote Count',
    'Hemizygote Count',
    'Variant ID'
]


def make_new_df(old_df):
    df = old_df[old_df['exome'].notnull()]
    reframe_data = []
    for row in range(len(df)):
        newarray = []
        newarray.append(df.iloc[row].get('gene_symbol')) # 1
        newarray.append(df.iloc[row].get('chrom')) # 2
        newarray.append(df.iloc[row].get('pos')) # 3
        newarray.append(df.iloc[row].get('rsid'))  # 4
        newarray.append(df.iloc[row].get('ref')) # 5
        newarray.append(df.iloc[row].get('alt')) # 6
        newarray.append(df.iloc[row].get('hgvsp')) # 7
        newarray.append(df.iloc[row].get('hgvsc')) # 8
        newarray.append(df.iloc[row].get('consequence')) # 9
        if df.iloc[row].get('flags'):
            newarray.append(df.iloc[row].get('flags')[0]) # 10
        else:
            newarray.append('')
        newarray.append(df.iloc[row].get('exome').get('ac')) # 11
        newarray.append(df.iloc[row].get('exome').get('an')) # 12
        newarray.append(df.iloc[row].get('exome').get('af')) # 13
        newarray.append(df.iloc[row].get('exome').get('ac_hom')) # 14
        newarray.append(df.iloc[row].get('exome').get('ac_hemi')) # 15
        newarray.append(df.iloc[row].get('variant_id')) # 16
        reframe_data.append(newarray)
    #add reframe_data and header
    new_df = pd.DataFrame(np.array(reframe_data), columns=header)
    return new_df

# generate and download csv file of each gene, saved to current path
def generate_csv(gene_id_list):
    for gene_id in gene_id_list:
        try:
            make_new_df(make_df(gene_id)).to_csv(gene_id + '.csv',index=False)    
            saved_list.append(gene_id)
            print('\x1b[6;30;42m' + 'Saved: ' + gene_id + '\x1b[0m')
        except:
            print('\x1b[6;30;41m' + 'Error: ' + gene_id + '\x1b[0m')
            pass

# download the combined csv file to current path, named as "output.csv"
def combine_csv():
    generate_csv(gene_id_list)
    combined_csv = pd.read_csv(saved_list[0] + '.csv')
    combined_csv.to_csv('output.csv', encoding="utf_8_sig", index=False)
    for gene_id in saved_list:
        combined_csv = pd.read_csv(gene_id + '.csv')
        combined_csv.to_csv('output.csv',encoding="utf_8_sig",index=False,header=False,mode='a+')
    print('Combining file...\n\x1b[6;30;42mConbined File to output.csv\x1b[6;30;41m\n')
    
#Please double check gene_name,
#then try enter the error gene_name in "https://gnomad.broadinstitute.org/"to check existence   
    
    
    


# In[15]:


combine_csv()


# In[ ]:




