import pandas as pd
df = pd.read_csv("heart.csv")

# Dropping irrelevant columns
df = df.drop(["id"], axis=1)

# Dropping unknown smoking status for non-children
a = df.loc[df["age"] < 18]
b = df.loc[df["age"] >= 18]
c = b.loc[b["smoking_status"] != "Unknown"]
df = pd.concat([a, c], ignore_index=True)

# Dropping nan values
for column in df.columns:
    df.dropna(subset=[column], inplace=True)

# Dropping gender values labeled other since only gender at birth can affect the result
df.drop(df.index[df["gender"] == "Other"], inplace=True)

# Replacing string values with integers to be able to run correlation test and create model.
df["gender"] = df["gender"].replace(["Male", "Female"], [0, 1])
df["ever_married"] = df["ever_married"].replace(["No", "Yes"], [0, 1])
df["work_type"] = df["work_type"].replace(["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
                                          [0, 1, 2, 3, 4])
df["Residence_type"] = df["Residence_type"].replace(["Urban", "Rural    "], [0, 1])
df["smoking_status"] = df["smoking_status"].replace(["never smoked", "formerly smoked", "smokes", "Unknown"],
                                                    [0, 1, 2, 3])
print(df.corr()[["stroke"]])
