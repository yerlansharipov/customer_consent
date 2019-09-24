# The Effect of Twitter Sentiments on Stock Valuation

As social media penetrates all aspects of our life, it is also reflects people opinion on particular problem, product or service. With that in mind we want to explore whether twitter sentiments affects on stock market valuation of company. The system leverages Google NLP API to extract user's consent and builds correlation between customer consent and stock market fluctuation.  

## The System Architecture
<img src=https://github.com/yerlansharipov/customer_consent/blob/master/arch.png width=1200/>


## Sample output

                 Date               Location                                               Text Score Magnitude
0 2019-09-24 01:34:52  Washington State, USA  Yep. Would be a cool competition between Unive...   0.4       0.8
1 2019-09-24 01:33:29             Dallas, TX  Very true. Perhaps a cold thruster equipped or...   0.5       1.1
2 2019-09-24 01:33:25              Indio, CA  : Congratulation to Boca Chica site !! It’s ye...   0.2       0.4
3 2019-09-24 01:31:35   Melbourne, Australia                                                : …   0.1       0.1
4 2019-09-24 01:30:54  Washington State, USA  Or the Starship should have the small craft in...   0.2       0.2
5 2019-09-24 01:28:48             Dallas, TX  No. A small craft should come first to do that...     0       0.4
6 2019-09-24 01:23:31             USA Global  : We're thrilled that our work bringing space ...   0.5       1.1
7 2019-09-24 01:20:50                         While you are bragging about ratings, why don'...     0       0.2
8 2019-09-24 01:18:01         Sacramento, CA  : And the winner is... + for multimedia covera...   0.3       0.3
9 2019-09-24 01:16:26              Iowa, USA                  And propellant depot on the moon!   0.1       0.1
