import pandas as pd
from gui import *

# reading the excel file from a specified location

path = r"C:\Users\iragr\PycharmProjects\power\Service BI Analyst - Home Assignment.xlsx"
db = pd.read_excel(path, header=0, index_col=0, sheet_name="Table 1").fillna(0)
inventory = pd.read_excel('Service BI Analyst - Home Assignment.xlsx', header=0, index_col=0, sheet_name="Table 2").fillna(0)

# creating an empty dictionary, which will hold key: value pairs from the compatibility list
compatibly_dict = {}


# this function iterates over the compatibility list and adds values to the compatibly_dict
def compatibly_dict_generator(power_key1, power_key2, is_compatible):
    if power_key1 not in compatibly_dict.keys():
        compatibly_dict[power_key1] = set()
    elif power_key1 in compatibly_dict.keys():
        #should i remove the key from the values list?
        if is_compatible != 0:
            compatibly_dict[power_key1].add(power_key2)


# extracting the "Power" from the components

def component_extractor(agent_input):
    return agent_input.split('-')[0]

# find all compatible "Powers" and their inventory.

def compatible_powers_inventory(power):
    for item in compatibly_dict[power]:
        print(item, inventory.loc[item,:])

# this function looks for the highest inventory per each power in the inventory list


def inventory_generator(power):
    max_value = max(inventory.loc[power, :])
    for item in compatibly_dict[power]:
        if max(inventory.loc[item, :]) > max_value:
            max_value = max(inventory.loc[item, :])
    return round(max_value, 2)

# creating a dynamic iterators for the compatibility list


width_of_compatibly_list = len(db.columns)
columns = db.columns
for power2 in range(width_of_compatibly_list):
    for power1 in db.index:
        compatibly_dict_generator(power1, columns[power2], db.loc[power1][power2])

is_gui_on = True
while is_gui_on:
    try:
        component = component_extractor(input("Please specify componenet: "))
        compatible_powers_inventory(component)
        print("Max inventory for component ", component, " is " , str(inventory_generator(component)))
        is_exit = input("To exit the program, press 'Exit', to enter another component, press 'Enter'")
        if is_exit.lower()=='exit':
            is_gui_on = False
    except KeyError:
        print("Componenet ", component, "is not found in the inventory")
        message_after_error = input("To exit, press 'exit', to enter another component, press 'Enter'")
        if message_after_error.lower()=='exit':
            is_gui_on = False
