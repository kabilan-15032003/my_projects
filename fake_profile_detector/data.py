from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_csv('train.csv')

X = df.drop(columns=['fake'])

Y = df['fake']

rf_classifier = RandomForestClassifier()

rf_classifier.fit(X, Y)

user_id = input('Enter the User_ID: ')
profile_pic = int(input('Enter whether account has profile or not (YES = 1, NO = 0): '))
fullname = input('Enter the fullname: ')
desc_len = len(input('Enter the description: '))
n_post = int(input('Enter the number of post: '))
n_followers = int(input('Enter the number of followers: '))
n_followings = int(input('Enter the number of following: '))
private = int(input('Enter whether account status (PRIVATE = 1, PUBLIC = 0): '))
url = int(input('Enter whether account has URL or NOT (YES = 1, NO = 0): '))

num_user = 0
for i in user_id:
    if i.isnumeric():
        num_user += 1

num_name = 0
for i in fullname:
    if i.isnumeric():
        num_name += 1

ratio = fuzz.ratio(user_id.lower(), fullname.lower())
if ratio > 50:
    similarity = 1
else:
    similarity = 0

if len(fullname) == 0:
    flag = 0
else:
    flag = num_name/len(fullname)

sample = {'profile pic': profile_pic,
          'nums/length username': num_user/len(user_id),
          'fullname words': len(fullname.split(' ')),
          'nums/length fullname': flag,
          'name==username': similarity,
          'description length': desc_len,
          'external URL': url,
          'private': private,
          '#posts': n_post,
          '#followers': n_followers,
          '#follows': n_followings
          }

if rf_classifier.predict(pd.DataFrame([sample])) == 0:
    print('Account is Real')
else:
    print('Account is Fake')
