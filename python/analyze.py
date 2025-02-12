import os
import subprocess
import pandas as pd
from tqdm import tqdm

# load frame metadata

bestOfPath = '../images/bestOf/'
paths = [bestOfPath+fname for fname in os.listdir(bestOfPath)]
frameInfo = []
for path in tqdm(paths):
    rawInfo = subprocess.check_output(['identify', '-verbose', path])
    rawInfo = str(rawInfo)
    rawInfo = rawInfo.replace(' ','')
    rawInfo = rawInfo.split('\\n')
    rawInfo = [{e.split(':')[0]: ':'.join(e.split(':')[1:])} for e in rawInfo if e != "'"]
    info = {}
    for d in rawInfo:
        info.update(d)
    frameInfo.append(info)

# process metadata
frameInfo = pd.DataFrame(frameInfo)

#drop all irrelevant columns:
frameInfo = frameInfo[[col for col in frameInfo.columns if col[0] not in [str(num) for num in range(10)]]]
relevantColumns = ['min','standarddeviation','kurtosis','entropy','Colors','Comment','filename','Filesize','Pixelspersecond']
frameInfo = frameInfo[relevantColumns]
frameInfo = frameInfo.set_index('filename')

# fix dtypes:
for col in ['min', 'standarddeviation']:
    frameInfo[col] = frameInfo.apply(lambda txt: float(txt[col].replace(')','').split('(')[1]), axis=1)

for col in ['kurtosis', 'entropy']:
    frameInfo[col] = frameInfo[col].astype('float')

frameInfo.Colors = frameInfo.Colors.astype(int)

frameInfo.Filesize = frameInfo.apply(lambda txt: int(txt['Filesize'].replace('B','')), axis=1)
frameInfo.Pixelspersecond = frameInfo.apply(lambda txt: float(txt['Pixelspersecond'].replace('MB','')), axis=1)

'''
Compute rank according to:
    - min: low is good
    - standarddeviation: high is good
    - kurtosis: low is good
    - entropy: high is good
    - Colors: high is good
    - Filesize: high is good
    - Pixelspersecond: low is good
Then show 20 top and bottom pics
Test for covariance of these variables
Check that no pictures were overlooked/wrongly classified
'''

