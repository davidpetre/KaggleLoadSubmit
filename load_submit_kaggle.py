import urllib
import os
import numpy as np
import pandas as pd

def CheckCredentials():
    credentials_path = os.path.join(os.path.expanduser('~'), '.kaggle','kaggle.json')
    if os.path.isfile(credentials_path):
        return True
    else:
        return False

class LoadDataset:
    def __init__(self, comp, train = 'train.csv', test = 'test.csv'):
        self.competition = comp
        self.trainname = train
        self.testname = test
        self.credentials_path = os.path.join(os.path.expanduser('~'), '.kaggle','kaggle.json')
    
      
    def download_data(self, path = None):
        if path is None:
            path = self.competition
        download_string = "kaggle competitions download -c " + self.competition + " -p " + path
        if CheckCredentials():
            print(download_string)
            os.system(download_string)
        else:
            print('Cannot download data, Kaggle credentials not found in '+self.credentials_path)
        
    
    def load_data(self, path = None, train = 'train.csv', test = 'test.csv'):
        if path is None:
            path = self.competition
        train_csv_path = os.path.join(path, train)
        test_csv_path = os.path.join(path, test)
        print(train_csv_path, test_csv_path)
        train = pd.read_csv(train_csv_path, index_col = 0)
        test = pd.read_csv(test_csv_path, index_col = 0)
        full = train.append(test)
        return train, test, full

class Submit:
    def __init__(self, estimator, comp, test_X, filename_stem):
        self.competition = comp
        self.estimator = estimator
        self.test_X = test_X
        self.filename_stem = filename_stem
        self.name = filename_stem + "_" + str(estimator)[:str(estimator).find('(')] + ".csv"
        return None
    
    
    def write_output_csv(self, columns):
        #the columns parameter contains a list of two strings, the column name of the output dataframe
        #print(self.test_X)
        pred_y = (self.estimator).predict(self.test_X)
        pred_y = np.array([int(n) for n in pred_y])
        out = pd.DataFrame({columns[0]: (self.test_X).index, columns[1]: (pred_y)})
        out.to_csv( self.name , index = False )
        print("Saved to", self.name)
 #       return name, str(estimator)
    
    def submission_string(self):
        features = str(self.test_X.columns)
        message = str(self.estimator) + r'\n' + features
        submit_string = 'kaggle competitions submit -c ' + self.competition + ' -f '+self.name + ' -m "' + message + r'"'
        return submit_string
    
    def submit_now(self):
        string = self.submission_string()
        if CheckCredentials():
            os.system(string)
            print("Submission done")
        else:
            print('Cannot submit, Kaggle credentials not found.')