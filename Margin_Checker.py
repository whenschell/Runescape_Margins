# -*- coding: utf-8 -*-
"""
Margin_Checker
Created on Sun Feb 17 18:50:09 2019
@author: Will

Creates a CSV to check current buy and sell prices of items in runescape

"""


#IMPORTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import urllib.request, json, pandas as pd, time, os #Importing necessary modules urllib.request grabs files from online
#pandas is a dataframe library
#time accesses time functions
#os accesses operating system functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cwd = os.getcwd() #Sets the current working directory
url = "https://rsbuddy.com/exchange/summary.json?ts=" + str(int(time.time())) #The link to OS Buddy's current JSON file ex. 'https://rsbuddy.com/exchange/summary.json?ts=1550600163'
response = urllib.request.urlopen(url) #Grabs OS Buddy's JSON file from online
data = json.loads(response.read()) #Sets the grabbed OS Buddy's JSON file as a variable
item_limits = pd.read_csv(cwd + r'\Items.csv') #Gets all of the items from the Items.csv file and creates a dataframe
item_list = dict() #Creating a dictionary to holds all of the item information from the JSON file
item_for_table = [] #Creating an empty list to hold all of the safe margins to make a dataframe later
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def refresh_data() : #Creates the tuples within the item_list dictionary from the JSON file ('data')
    for key in data : #For every unique item
        item_name = data[key]['name'] #Sets the item name for every item based on JSON variable 'name'
        item_sell = data[key]['sell_average'] #Sets the current sell price for the item based on JSON variable 'sell_average'
        item_buy = data[key]['buy_average'] #Sets the current buy price for the item based on JSON variable 'buy_average'
        item_sell_quant = data[key]['sell_quantity'] #Sets the current sell quantity for the item based on JSON variable 'sell_quantity'
        item_buy_quant = data[key]['buy_quantity'] #Sets the current buy quantity for the item based on JSON variable 'buy_quantity'
        offer_safety = 'Not Safe' #Sets the default flip safety as 'Not Safe'
        sell_holder = 0 #Creates a default sell_holder to hold the sell price in case the 'item_sell' is lower than the 'item_buy' value
        buy_holder = 0 #Creates a default buy_holder to hold the buy price in case the 'item_buy' is higher than the 'item_sell' value
        buy_limit = 0 #Creates and sets the default 'buy_limit' to 0
        profit = 0 #Creates and sets the default 'profit' to 0
        total_profit = 0 #Creates and sets the default 'total_profit' to 0 ('total_proft' = 'profit' * 'buy_limit')
        gold_needed = 0 #Creates and sets the default 'gold_needed' to 0 ('gold_needed' = 'item_buy' * 'buy_limit')
        item_list[item_name] = [item_name, item_buy, item_sell, item_buy_quant, item_sell_quant, offer_safety, buy_holder, sell_holder, buy_limit, profit, total_profit, gold_needed] #adds each item to the item_list dictionary with their name as the key. Each item has the variables on the right side of the equals sign

def check_margin(item, limit) : #Checks if the margin gaps are safe, if there are enough offers, and sets the purchasing and selling prices for every item
    info = item_list[item]
    info[8] = limit
    #Makes sure that items have buy and sell values. Also ensures that at least half of the buy limit is being actively offered
    if (info[1] > 0 and info[2] > 0 and info[3] >= (limit/4) and info[4] >= (limit/4)) :
        info[5] = 'Consider'
        if (info[1] < info[2]) :
            info[6] = info[1]
            info[7] = info[2]
            info[1] = info[6]
            info[2] = info[7]
            info.pop(7)
            info.pop(6)
        elif (info[2] < info[1]) :
            info[6] = info[2]
            info[7] = info[1]
            info[1] = info[6]
            info[2] = info[7]
            info.pop(7)
            info.pop(6)
        else :
            info[5] = 'No Gap'
            info.pop(7)
            info.pop(6)
    else :
        info[5] = 'Not Safe'
        info.pop(7)
        info.pop(6)
        
    if (len(info) == 10 and info[5] == 'Consider') :
        info[1] = info[1] + int(info[1] * 0.025)
        info[2] = info[2] - int(info[2] * 0.025)
        if (info[2] > info[1]) :
            info[5] = 'Safe'
            info[7] = info[2] - info[1]
            info[8] = info[7] * info[6]
            info[9] = info[1] * info[6]
            item_for_table.append(info)
        else :
            info[5] = 'Not Safe'          
    else :
        info[5] = 'Not Safe'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#SCRIPTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
refresh_data() #Creating the initial item_list from the JSON file ('data')  
for Item_Name, row in item_limits.iterrows():
    check_margin(row['Item'], row['Limit'])
margin_table = pd.DataFrame(item_for_table, columns = ['Item_Name', 'Buy_Price', 'Sell_Price', 'Buy_Quant', 'Sell_Quant', 'Safety', 'Buy_Limit', 'Profit', 'Total_Profit', 'Gold_Needed'])
margin_table.sort_values(["Total_Profit"], axis = 0, ascending = False, inplace = True, na_position = 'last')
margin_table.to_csv(cwd + r'\Margins.csv')
os.startfile(cwd + r'\Margins.csv')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        
        
    
        
    
        
    