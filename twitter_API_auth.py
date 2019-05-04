import tweepy as tw

consumer_key='Ao50lha2TpmFwItcoCZBdCkSu'
consumer_secret='9hjTrfap4aReMjTzvVpP3sAYIX4Q8TTIhh4Gx09nDXDiUd8Ued'
access_token='1123994014515118081-3kbdwTu871OdscqFPjTpr7WPcRk1Fs'
access_token_secret='HJaMVDgHXAU0ndDCP2dHCpidXn5zGimnA9Zo86qGby5Uw'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
