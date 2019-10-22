#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
import pandas as pd


# In[10]:


# type the gene's name in the gene_id_list here!!
gene_id_list = [
    "OR52M1", "OR55", "OR52N4", "OR11H1", "OR4K15", "OR6S1", "OR5AP2",
    "OR5H1", "OR13C1", "OR2K2", "OR8G5", "OR1L3", "OR2T27"
]
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

# add the gene_id at the last column! 
def make_df(gene_id):
    li = get_variant_list(gene_id)
    df = pd.DataFrame(li)
    df['SYMBOL'] = gene_id
    return df


def make_csv(df, gene_id):
    df.to_csv(gene_id + '.csv')

# generate and download csv file of each gene, saved to current path
def generate_csv(gene_id_list):
    for gene_id in gene_id_list:
        try:
            foo = get_variant_list(gene_id)
            gene_df = make_df(gene_id)
            make_csv(gene_df, gene_id)
            saved_list.append(gene_id)
            print('\x1b[6;30;42m' + 'saved: ' + gene_id + '\x1b[0m')
        except:
            print('\x1b[6;30;41m' + 'error: ' + gene_id + '\x1b[0m')
            pass

# download the combined csv file to current path, named as "output.csv"
def combine_csv():
    generate_csv(gene_id_list)
    combined_csv = pd.read_csv(saved_list[0] + '.csv')
    combined_csv.to_csv('output.csv', encoding="utf_8_sig", index=False)
    for gene_id in saved_list:
        combined_csv = pd.read_csv(gene_id + '.csv')
        combined_csv.to_csv('output.csv',
                            encoding="utf_8_sig",
                            index=False,
                            header=False,
                            mode='a+')
    print('combined file: \x1b[6;30;42m output.csv \x1b[6;30;41m')


# In[11]:


combine_csv()


# In[ ]:




