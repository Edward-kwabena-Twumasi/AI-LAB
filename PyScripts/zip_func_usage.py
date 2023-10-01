
keys = ["Name","Age","Race"]
names = ['Edward','Johnson','Fynn']
ages =['24','29','23']
races = ['black','white','white']

df_dict = {key: values for key, values in zip(keys, [names, ages, races])}

print(df_dict)