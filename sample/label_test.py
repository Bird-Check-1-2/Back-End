import pandas as pd

df = pd.read_csv("sample/labelled_bird_sample.csv")

hummingbirds = df[df['name'] == "Ruby-throated Hummingbird"]

hummingbirds = hummingbirds[hummingbirds['region'] == "Appohzarka"]
print(hummingbirds[['name', 'season', 'region', 'seas_reg_rare']].head(25))