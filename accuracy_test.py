import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

df = pd.read_csv("heart.csv")

# Dropping irrelevant columns
df = df.drop(["id", "gender", "Residence_type"], axis=1)

# Dropping unknown smoking status for non-children
a = df.loc[df["age"] < 18]
b = df.loc[df["age"] >= 18]
c = b.loc[b["smoking_status"] != "Unknown"]
df = pd.concat([a, c], ignore_index=True)
df["ever_married"] = df["ever_married"].replace(["No", "Yes"], [0, 1])
df["work_type"] = df["work_type"].replace(["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
                                              [0, 1, 2, 3, 4])
df["smoking_status"] = df["smoking_status"].replace(["never smoked", "formerly smoked", "smokes", "Unknown"],
                                                        [0, 1, 2, 3])

# Dropping nan values
for column in df.columns:
    df.dropna(subset=[column], inplace=True)

# Splitting input and output sets
had_stroke = df.loc[df["stroke"] == 1]
had_stroke = had_stroke.drop("stroke", axis=1)
X = df.drop("stroke", axis=1)
y = df["stroke"]

# Regression process
reg = linear_model.LinearRegression()
reg.fit(X, y)
predicted_stroke = reg.predict(had_stroke)
ps_df = pd.DataFrame(predicted_stroke)
ps_df.columns = ["Predicted Score"]
d = ps_df.loc[ps_df["Predicted Score"] > 0.05]
e = len(d.count(axis='columns'))
f = len(ps_df.count(axis='columns'))
print(f"Percentage of people who are in risk of stroke according to model in people who had a stroke = % {e / f * 100}")