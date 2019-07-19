#!/usr/bin/env python
# coding: utf-8

# In[17]:


import xml.etree.ElementTree as ElementTree
import pandas as pd
import csv

dfcols = ['source', 
          'url', 
          'title', 
          'image',
          'category',
          'description',
          'rank',
          'pubdate',
          'video'
         ]

def getvalueofnode(node):
    """ return node text or None """
    return node.text if node is not None else None

count = 0
with open("newsspace200.xml") as file:
# with open("newsSpace.sample") as file:
    with open("newsSpace.parsed", "w") as dest:
        wr = csv.writer(dest)
        for line in file:
            try:
                line = "<example>"+line[:-1]+"</example>"
                root = ElementTree.fromstring(line)
                
                source = root.find('source')
                url = root.find('url')
                title = root.find('title')
                image = root.find('image')
                category = root.find('category')
                description = root.find('description')
                rank = root.find('rank')
                pubdate = root.find('pubdate')
                video = root.find('video')
                
                csv_line = [getvalueofnode(source),
                                getvalueofnode(url),
                                getvalueofnode(title),
                                getvalueofnode(image),
                                getvalueofnode(category),
                                getvalueofnode(description),
                                getvalueofnode(rank),
                                getvalueofnode(pubdate),
                                getvalueofnode(video)
                              ]
                wr.writerow(csv_line)
                count = count + 1
                if count % 50000 == 0:
                    print("written:", count)
            except Exception as e: 
                print(e)
                continue


# In[19]:


newsspace = pd.read_csv("newsSpace.parsed", header=None, names=dfcols)
newsspace


# In[41]:


newsspace["feature"] = newsspace.title + "|" + newsspace.description


# In[42]:


classes = newsspace.groupby(["category"]).count()[["source"]].sort_values("source", ascending=False).reset_index()
top4_classes = classes.head(4)["category"]
top4_classes


# In[43]:


train_test = newsspace[newsspace.category.isin(top4_classes)].groupby("category").head(31900)
train_test


# In[49]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_test.feature, train_test.category, train_size=30000, test_size=1900, random_state=42)


# In[50]:


pd.DataFrame({"feature":X_train, "label": y_train}).to_csv("train.tsv", sep="\t")


# In[51]:


pd.DataFrame({"feature":X_test, "label": y_test}).to_csv("test.tsv", sep="\t")


# In[ ]:




