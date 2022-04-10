import requests
import pandas as pd

with open('bearer.txt', 'r') as f:
    bearer_token = f.read()

headers = {'Authorization': 'Bearer ' + bearer_token}
next_token = None
tweets = []
keyword = 'wojna'

for i in range(100):
    params = {'query': '#' + keyword,
              'max_results': 100,
              'tweet.fields': 'created_at,referenced_tweets',
              'next_token': next_token}
    r = requests.get('https://api.twitter.com/2/tweets/search/recent', headers=headers, params=params)
    print(r.status_code)
    for tweet in r.json()['data']:
        try:
            type = tweet['referenced_tweets'][0]['type']
            if type == 'retweeted':
                continue
        except KeyError:
            pass
        created = tweet['created_at']
        id = tweet['id']
        text = tweet['text']
        tweets.append([created, id, text])
    try:
        next_token = r.json()['meta']['next_token']
    except KeyError:
        break

df = pd.DataFrame(tweets, columns=['Created', 'ID', 'Text'])
df.to_csv(keyword + '.csv', index=False)
