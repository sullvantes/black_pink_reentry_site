import os
import pandas as pd
import numpy as np

from sodapy import Socrata

chi_domain = 'data.cityofchicago.org'
chi_city_owned_land_identifier = 'aksk-kvfp'
chi_client = Socrata(chi_domain, None)

chi_city_owned_land_results =chi_client.get(chi_city_owned_land_identifier, limit = 10000000000)
# print chi_city_owned_land_results
counter = 0
for permit in chi_city_owned_land_results:
    counter += 1 
    # print permit,"\n"
    # print permit['digit_pin'], permit['location']['human_address']

print counter
chi_df = pd.DataFrame.from_dict(chi_city_owned_land_results)
# print(chi_df.shape)

# In[11]:


# extract tree-related complaints
# tree_related = pd.concat([
#     nyc_df.complaint_type.str.contains(r'[T|t]ree').value_counts(),
#     chatt_df.description.str.contains(r'[T|t]ree').value_counts()
# ], axis=1, keys=['nyc', 'chatt'])
# tree_related.div(tree_related.sum()).round(2)


# Looks like trees are a higher percentage of NYC complaints than Chattanooga's.
#
# Note that we can only talk about percentages, since our query results got truncated to 1,000 rows.
#
# What if we want to be smarter about what we ask for, so that we can get 100% of the subset of data
# we're most interested in? That's the subject of a future example, so stay tuned!
#
# If you want to find more data sets, here's Socrata's data finder:
#
# https://www.opendatanetwork.com/search