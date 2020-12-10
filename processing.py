import numpy as np
import pandas as pd

def avg(df):
  benign = pd.read_csv('benign.csv')
  benign.columns = ['number','isic_id','benign_malignant']

  for row in benign:
    if row['isic_id'] ==  