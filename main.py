import pandas as pd
from sklearn import linear_model


def conversion():
    # Replacing string values with integers to be able to run correlation test and create model.
    df["ever_married"] = df["ever_married"].replace(["No", "Yes"], [0, 1])
    df["work_type"] = df["work_type"].replace(["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
                                              [0, 1, 2, 3, 4])
    df["smoking_status"] = df["smoking_status"].replace(["never smoked", "formerly smoked", "smokes", "Unknown"],
                                                        [0, 1, 2, 3])
    user_df["hypertension"] = user_df["hypertension"].replace(["no", "yes"], [0, 1])
    user_df["heart_disease"] = user_df["heart_disease"].replace(["no", "yes"], [0, 1])
    user_df["ever_married"] = user_df["ever_married"].replace(["no", "yes"], [0, 1])
    user_df["work_type"] = user_df["work_type"].replace(
        ["private", "self employed", "govt job", "children", "never worked"], [0, 1, 2, 3, 4])
    user_df["smoking_status"] = user_df["smoking_status"].replace(["never smoked", "formerly smoked", "smoking"],
                                                                  [0, 1, 2])


def regression():
    # Defining training set.
    X = df.drop(["stroke"], axis=1)
    y = df.pop("stroke")

    # Creating the model
    reg = linear_model.LinearRegression()
    reg.fit(X, y)
    predicted_stroke = reg.predict(user_df)
    if predicted_stroke > 0.20:
        print(f"Your predicted stroke score is {predicted_stroke}. Which is higher than '0.20' threshold.")
        print("You're very likely to have a stroke in near future. See a doctor and take needed precautions "
              "immediately.")
    elif predicted_stroke > 0.13:
        print(f"Your predicted stroke score is {predicted_stroke}. Which is between '0.13' and '0.20'.")
        print("You're in significant risk to have a stroke. See a doctor in your first opportunity.")
    elif predicted_stroke > 0.05:
        print(f"Your predicted stroke score is {predicted_stroke}. Which is between '0.05' and '0.13'.")
        print("You may have a threat of having a stroke in foreseeable future. Consider seeing a doctor in your free "
              "time to get additional testing.")
    else:
        print(f"Your predicted stroke score is {predicted_stroke}. Which is lower than '0.05' threshold.")
        print("You're not in any of the risk groups for now. Have a healthy life!")


df = pd.read_csv("heart.csv")

# Dropping irrelevant columns
df = df.drop(["id", "gender", "Residence_type"], axis=1)

# Dropping unknown smoking status for non-children
a = df.loc[df["age"] < 18]
b = df.loc[df["age"] >= 18]
c = b.loc[b["smoking_status"] != "Unknown"]
df = pd.concat([a, c], ignore_index=True)

# Dropping nan values
for column in df.columns:
    df.dropna(subset=[column], inplace=True)


# Taking inputs from user and applying the model
i = 0
while i == 0:
    booting = input("Type 'info' to learn about valid input types, type 'start' to start.\n")
    if booting.casefold() == "info":
        print("Valid input types:")
        print("Age: Any Integer Value")
        print("Hypertension: 'Yes' or 'No'")
        print("Heart Disease: 'Yes' or 'No'")
        print("Ever Married: 'Yes' or 'No'")
        print("Work Type: 'Children', 'Govt Job', 'Never Worked', 'Private' or 'Self Employed'")
        print("Body Mass Index: Any Float Value")
        print("Smoking Status: 'Formerly Smoked', 'Never Smoked', 'Smoking'\n\n\n")
    elif booting.casefold() == "start":
        i = 1
        while i == 1:
            user_age = (input("Enter your age: "))
            if not user_age.isdigit():
                i = 1
                print("Age must be an integer.")
            else:
                i = 2
                user_age = int(user_age)
        while i == 2:
            user_ht = input("Do you have hypertension?: ").casefold()
            if user_ht != "yes" and user_ht != "no":
                i = 2
                print("Answer must be 'Yes' or 'No'.")
            else:
                i = 3
        while i == 3:
            user_hd = input("Do you have a heart disease?: ").casefold()
            if user_hd != "yes" and user_hd != "no":
                i = 3
                print("Answer must be 'Yes' or 'No'.")
            else:
                i = 4
        while i == 4:
            user_em = input("Did you ever get married?: ").casefold()
            if user_em != "yes" and user_em != "no":
                i = 4
                print("Answer must be 'Yes' or 'No'.")
            else:
                i = 5
        while i == 5:
            user_wt = input("What's your work type?: ").casefold()
            if user_wt != "children" and user_wt != "govt job" and user_wt != "never worked" and\
                    user_wt != "private" and user_wt != "self employed":
                i = 5
                print("Answer must be 'Children', 'Govt Job', 'Never Worked', 'Private' or 'Self Employed'.")
            else:
                i = 6
        while i == 6:
            user_bmi = (input("What's your Body Mass Index?: "))
            if user_bmi.isalpha() or (user_bmi.isalnum() and not user_bmi.isdigit()):
                i = 6
                print("BMI value must be a float.")
            else:
                i = 7
                user_bmi = float(user_bmi)
        while i == 7:
            user_ss = input("What's your smoking status?: ").casefold()
            if user_ss != 'formerly smoked' and user_ss != 'never smoked' and user_ss != 'smoking':
                i = 7
                print("Answer must be 'Formerly Smoked' or 'Never Smoked' or 'Smoking'")
            else:
                i = 8
        while i == 8:
            user_gl = input("What's the average glucose level in your blood?: ")
            if user_gl.casefold() == "unknown":
                i = 9
                # Creating training dataframe without AVL column
                df = df.drop(["avg_glucose_level"], axis=1)

                # Creating dataframe for testing with user inputs
                user_inputs = {'age': [user_age], 'hypertension': [user_ht],
                               'heart_disease': [user_hd], 'ever_married': [user_em], 'work_type': [user_wt],
                               'bmi': [user_bmi], 'smoking_status': [user_ss]}

                user_df = pd.DataFrame(user_inputs)

                # Applying conversion and modeling with pre-defined functions
                conversion()
                regression()
            elif user_gl.isalpha() or (user_gl.isalnum() and not user_gl.isdigit()):
                print("AGL value must be a float or 'Unknown'")
                i = 8
            else:
                i = 9

                # Creating dataframe for testing with user inputs
                user_inputs = {'age': [user_age], 'hypertension': [user_ht],
                               'heart_disease': [user_hd], 'ever_married': [user_em], 'work_type': [user_wt],
                               'avg_glucose_level': [user_gl], 'bmi': [user_bmi],
                               'smoking_status': [user_ss]}

                user_df = pd.DataFrame(user_inputs)

                # Applying conversion and modeling with pre-defined functions
                conversion()
                regression()
    else:
        print("Invalid input. Valid inputs are 'info' and 'start'.\n\n\n")
