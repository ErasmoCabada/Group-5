import pandas as pd
import matplotlib.pyplot as plt

#load csv
csv_path = "data/file_rootbeer_touches.csv"
df = pd.read_csv(csv_path)

# convert touches to datetime
df["Touch_Date"] = pd.to_datetime(df["Touches"])

# Find min and max dates and total weeks
min_date = df["Touch_Date"].min()
max_date = df["Touch_Date"].max()
# total weeks from start
df["weeks_total"] = (df["Touch_Date"] - min_date).dt.days // 7

#generate unique number for each author
authors = df["Author"].unique()

df["file_id"] = df["Filename"].astype("category").cat.codes

# scatter plot
for author in authors:
    author_data = df[df["Author"] == author]
    plt.scatter(
        author_data["file_id"],
        author_data["weeks_total"],
    )

plt.ylabel("Weeks")
plt.xlabel("Files")
plt.show()