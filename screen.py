#! /usr/bin/python

# Welcome to the Dopeler Value Investing pre-screening tool.
# Yes, the name Dopeler is inspired by the movie _Snow Day_.

# Dopeler Value Investing only a pre-screening tool to identify the stocks that appear to be most promising.
# This is NOT a replacement for the more detailed Doppler Value Investing analysis.
# The purpose of Dopeler Value Investing is to quickly process financial information on thousands of stocks.
# Stocks that are clearly incompatible with the Doppler Value Investing philosophy can be quickly screened out.
# Attention can be focused on the most promising stocks.

# Please note that not all stocks that look attractive in the Dopeler Value Investing screen are suitable.
# Some may be beneficiaries of the high point in the industry cycle.
# Some may be the beneficiaries of a temporary fad.
# In addition, there may be other problems with some of these stocks.

import sys
import os
import csv
import datetime
import urllib2
import time, random
import urllib
import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import re
from HTMLParser import HTMLParser

dir_analysis = os.getcwd()
os.chdir('..')
dir_doppler = os.getcwd()
dir_input = dir_doppler + '/screen-input'
dir_output = dir_doppler + '/screen-output'
os.chdir(dir_analysis)

##############################################################################################
# PART 1: For a given exchange, obtain a list of ticker symbols for stocks that are NOT funds.
##############################################################################################

# Purpose: extract a given column from a 2-D list
# Input: 2-D data list
# Output: 1-D data list representing the (n_local+1) -th column of the input list
def column (list_input, n_input):
    list_transpose = zip (*list_input)
    return list_transpose [n_input]

# Purpose: extract a given column from a 2-D list but omit the top row
# Input: 2-D data list
# Output: 1-D data list representing the (n_local+1) -th column of the input list, minus the first entry
def column_data (list_input, n_input):
    list1 = column (list_input, n_input)
    list2 = list1 [1:]
    return list2

# Purpose: count the number of columns in a 2-D list
# Input: 2-D data list
# Output: integer representing the number of columns of the 2-D list
def num_of_columns (list_input):
    list_transpose = zip (*list_input)
    n_local = len (list_transpose)
    return n_local

# Purpose: get the first row in a 2-D list
# Input: 2-D data list
# Output: 1-D data list
def list_titles (list_input):
    list_output = list_input [0][0:]
    return list_output

# Purpose: get the column number corresponding to a title
# Input: 2-D data list
# Output: integer
def col_num_title (list_input, string_input):
    list_1d = list_titles (list_input)
    n = 0
    n_final = len (list_1d) - 1
    while n <= n_final:
        if (list_1d [n] == string_input):
            return n
        n = n + 1
    return None 

# Purpose: get the column corresponding to a title
# Input: 2-D data list
# Output: 1-D data list of strings
def col_title (list_input, string_input):
    col_num_local = col_num_title (list_input, string_input)
    list_output = column_data (list_input, col_num_local) 
    return list_output

# Purpose: Convert a string to a floating point number
# Input: string
# Output: floating point number
def str_to_float (string_input):
    try:
        x = float (string_input)
    except:
        x = None
    return x

# This defines the class CSVfile (filename).
# Input: name of csv file
# Output: 2-D list fed by the input file
class CSVfile:
    def __init__ (self, filename):
        self.filename = filename

    def filelist (self):
        locallist = []
        with open (self.filename, 'rb') as f:
            reader = csv.reader (f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for row in reader:
                locallist.append (row)
        return locallist

# This defines the class Exchange (exch_abbrev)
# Input: 'nyse', 'amex', or 'nasdaq'
# Outputs: 2-D data list
class Exchange:
    def __init__ (self, exch_abbrev):
        self.exch_abbrev = exch_abbrev

    # Purpose: reads the contents of the file containing the list of stocks and information on each stock
    # Input: file containing list of stocks
    # Output: 2-D data list
    def data (self):
        file_stock = CSVfile (dir_input + '/companylist-' + self.exch_abbrev + '.csv')
        list_stock = file_stock.filelist ()
        return list_stock

    # Purpose: get list of all entries in a column with a given title
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def column_all (self, string_input):
        list_input = self.data ()
        list_titles_local = list_titles (list_input)
        num_col_symbol = col_num_title (list_input, string_input)
        list_output = column_data (list_input, num_col_symbol)
        return list_output
        
    # Purpose: get a list of the symbols for all of the stocks profiled
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def symbol_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'Symbol')
        return list_output

    # Purpose: get a list of the sectors for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def sector_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'Sector')
        return list_output

    # Purpose: get a list of the industries for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def industry_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'industry')
        return list_output

    # Purpose: get a list of the names for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def name_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'Name')
        return list_output

    # Purpose: get a list of the prices for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def price_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'LastSale')
        return list_output

    # Purpose: get a list of the market caps for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def marketcap_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'MarketCap')
        return list_output

    # Purpose: get a list of the index number for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list
    def index_all (self):
        list1 = self.data ()
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        list_output = []
        while n <= n_last:
            list_output.append (n)
            n = n + 1
        return list_output

    # Purpose: get a list of the index numbers for each stock that is NOT a fund
    # Inputs: 1-D data lists 
    # Output: 1-D data list
    def index_selected (self):
        list1 = self.sector_all ()
        list2 = self.industry_all ()
        list3 = self.index_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        list_output = []
        while n <= n_last:
            if (list1 [n] <> "n/a" ) & (list2 [n] <> "n/a" ):
                list_output.append (list3 [n])
            n = n + 1
        return list_output

    # Purpose: get a list of the ticker symbols for each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list 
    def symbol_selected (self):
        list1 = self.index_selected ()
        list2 = self.symbol_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            symbol1 = list2 [i_select]
            symbol1 = symbol1.replace (' ', '') # Eliminate spaces
            symbol1 = symbol1.replace ('/', '.') # Replace slash with period
            list_output.append (symbol1) 
            n = n + 1
        return list_output

    # Purpose: get a list of the names of each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list
    def name_selected (self):
        list1 = self.index_selected ()
        list2 = self.name_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            name1 = list2 [i_select]
            list_output.append (name1) 
            n = n + 1
        return list_output

    # Purpose: get a list of the prices of each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list of numbers
    def price_selected (self):
        list1 = self.index_selected ()
        list2 = self.price_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            price_str = list2 [i_select]
            price_num = str_to_float (price_str)
            list_output.append (price_num) 
            n = n + 1
        return list_output

    # Purpose: get a list of the market caps of each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list of numbers
    def marketcap_selected (self):
        list1 = self.index_selected ()
        list2 = self.marketcap_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            marketcap_str = list2 [i_select]
            marketcap_num = str_to_float (marketcap_str)
            list_output.append (marketcap_num) 
            n = n + 1
        return list_output

    # Purpose: get a list of the number of shares outstanding for each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list of numbers
    def nshares_selected (self):
        list1 = self.marketcap_selected ()
        list2 = self.price_selected ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            marketcap1 = list1 [n]
            price1 = list2 [n]
            try:
                nshares1 = round(marketcap1/price1)
            except:
                nshares1 = None
            list_output.append (nshares1) 
            n = n + 1
        return list_output

    # Purpose: get a list of the sectors of each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list
    def sector_selected (self):
        list1 = self.index_selected ()
        list2 = self.sector_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            sector1 = list2 [i_select]
            list_output.append (sector1) 
            n = n + 1
        return list_output

    # Purpose: get a list of the industries of each stock that is NOT a fund
    # Inputs: 1-D data lists
    # Output: 1-D data list
    def industry_selected (self):
        list1 = self.index_selected ()
        list2 = self.industry_all ()
        list_output = []
        n_length = len (list1)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            i_select = list1 [n]
            industry1 = list2 [i_select]
            list_output.append (industry1) 
            n = n + 1
        return list_output

#######################################################################################################################
# PART 2: Using Exchange.symbol_selected, compile the list of ticker symbols from the AMEX, NYSE, and NASDAQ exchanges.
#######################################################################################################################
print "******************************"
print "BEGIN acquiring list of stocks"

# BEGIN: this section is for testing purposes

Exchange1 = Exchange ('test')
list_symbol = Exchange1.symbol_selected ()
list_name = Exchange1.name_selected ()
list_price = Exchange1.price_selected ()
list_nshares = Exchange1.nshares_selected ()
list_sector = Exchange1.sector_selected ()
list_industry = Exchange1.industry_selected ()

# END: this section is for testing purposes

# BEGIN: enable this section for analyzing all AMEX, NYSE, and NASDAQ stocks

Exchange1 = Exchange ('amex')
Exchange2 = Exchange ('nyse')
Exchange3 = Exchange ('nasdaq')

list_symbol = Exchange1.symbol_selected () + Exchange2.symbol_selected () + Exchange3.symbol_selected ()
list_name = Exchange1.name_selected () + Exchange2.name_selected () + Exchange3.name_selected ()
list_price = Exchange1.price_selected () + Exchange2.price_selected () + Exchange3.price_selected ()
list_nshares = Exchange1.nshares_selected () + Exchange2.nshares_selected () + Exchange3.nshares_selected ()
list_sector = Exchange1.sector_selected () + Exchange2.sector_selected () + Exchange3.sector_selected ()
list_industry = Exchange1.industry_selected () + Exchange2.industry_selected () + Exchange3.industry_selected ()

# END: enable this section for analyzing all AMEX, NYSE, and NASDAQ stocks

num_stocks = len (list_symbol)
print "Total number of stocks: " + str(num_stocks)
print "FINISHED acquiring list of stocks"
print "*********************************"

############################################################
# PART 3: For each stock, download the financial data needed
############################################################
# NOTE: Downloading is bypassed if the file to be replaced is less than 4 days old.  
# NOTE: Delay is used to avoid overwhelming the servers.

# Getting financial figures from CNBC (more data than Yahoo, capable of handling big loads)
URL_BASE_SMARTMONEY = 'http://www.smartmoney.com/quote/'
LOCAL_BASE = dir_doppler + '/screen-downloads'

# Smart Money URL for balance sheet data
def url_balancesheet (symbol1):
    url1 = URL_BASE_SMARTMONEY + symbol1 
    url1 = url1 + '/?story=financials&timewindow=1&opt=YB&isFinprint=1&framework.view=smi_emptyView'
    return url1

# Smart Money URL for income statement data
def url_income (symbol1):
    url1 = URL_BASE_SMARTMONEY + symbol1
    url1 = url1 + '/?story=financials&timewindow=1&opt=YI&isFinprint=1&framework.view=smi_emptyView'
    return url1

# Smart Money URL for cash flow statement data
def url_cashflow (symbol1):
    url1 = URL_BASE_SMARTMONEY + symbol1
    url1 = url1 + '/?story=financials&timewindow=1&opt=YC&isFinprint=1&framework.view=smi_emptyView'
    return url1

def local_root (symbol1):
    url1 = LOCAL_BASE + '/' + symbol1
    return url1

def local_balancesheet (symbol1):
    url1 = local_root (symbol1) + '/balancesheet.html'
    return url1

def local_income (symbol1):
    url1 = local_root (symbol1) + '/income.html'
    return url1

def local_cashflow (symbol1):
    url1 = local_root (symbol1) + '/cashflow.html'
    return url1

# Create directory path1 if it does not already exist
def create_dir (path1):
    if not (os.path.exists(path1)):
        os.mkdir (path1)

# Get age of file
# Based on solution at 
# http://stackoverflow.com/questions/5799070/how-to-see-if-file-is-older-than-3-months-in-python
# Returns 1000000 if the file does not exist
def age_of_file (file1): # In days
    today = datetime.datetime.now ()
    try:
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(file1))
        age = today - modified_date
        return age.days
    except:
        return 1000000

# Download information on a given stock
def download_data (symbol1):
    from urllib2 import Request, urlopen, URLError, HTTPError
    url1 = url_balancesheet (symbol1)
    url2 = url_income (symbol1)
    url3 = url_cashflow (symbol1)
    local1 = local_balancesheet (symbol1)
    local2 = local_income (symbol1)
    local3 = local_cashflow (symbol1)    

    print "Downloading data on " + symbol1

    # Download balance sheet information
    url = url1
    file_name = local1
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading balance sheet data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .5))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"

    # Download income information
    url = url2
    file_name = local2
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading income statement data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .5))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"

    # Download cash flow information
    url = url3
    file_name = local3
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading cash flow data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .5))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"
    
create_dir (LOCAL_BASE) # Create screen-downloads directory if it does not already exist
i_stock = 0
i_stock_max = len (list_symbol)
start = time.time ()
for symbol in list_symbol:
    create_dir (local_root (symbol)) # Create directory for stock if it does not already exist
    download_data (symbol)
    i_stock = i_stock + 1

    now = time.time ()
    t_elapsed = now - start
    rate_s = i_stock / t_elapsed # Stocks/second
    remain_s = (i_stock_max - i_stock)/rate_s
    remain_m = int (round(remain_s/60))
    print "Download completion: " + str(i_stock) + '/' + str(i_stock_max) + "; " + str(remain_m) + " minutes remaining"

    
###############################################################
# PART 4: For each stock, process the financial data downloaded
###############################################################

# Purpose: Obtain data for a specific line item on the balance sheet
# Inputs: two strings (one of the symbol, one for the title of the line item)
# Output: list of numbers for the line item
def list_line_balance (symbol_input, title_input):
    url_local = local_balancesheet (symbol_input)
    page = urllib.urlopen (url_local)
    soup = BeautifulSoup (page)
    soup_line_item = soup.findAll(text=title_input)[0].parent.parent.parent
    list_output = soup_line_item.findAll('td') # List of elements
    list_output = clean_list (list_output)
    return list_output

# Purpose: Obtain data for a specific line item on the cash flow statement
# Inputs: two strings (one of the symbol, one for the title of the line item)
# Output: list of numbers for the line item
def list_line_cashflow (symbol_input, title_input):
    url_local = local_cashflow (symbol_input)
    page = urllib.urlopen (url_local)
    soup = BeautifulSoup (page)
    soup_line_item = soup.findAll(text=title_input)[0].parent.parent.parent
    list_output = soup_line_item.findAll('td') # List of elements
    list_output = clean_list (list_output)
    return list_output

# Purpose: Obtain data for a specific line item on the income statement
# Inputs: two strings (one of the symbol, one for the title of the line item)
# Output: list of numbers for the line item
def list_line_income (symbol_input, title_input):
    url_local = local_income (symbol_input)
    page = urllib.urlopen (url_local)
    soup = BeautifulSoup (page)
    soup_line_item = soup.findAll(text=title_input)[0].parent.parent.parent
    list_output = soup_line_item.findAll('td') # List of elements
    list_output = clean_list (list_output)
    return list_output

# Purpose: Remove the HTML tags, commas, and spaces from an element in a list; used for processing financial data
# Input: 1-D list of BeautifulSoup.Tag
# Output: 1-D list of numbers
def clean_list (list_input):
    list_output = []
    n_length = len (list_input)
    n_last = n_length -1
    n = 0
    while n <= n_last:
        item_tag = list_input [n]
        item_string = str (item_tag) # Convert from type BeautifulSoup.Tag to type string
        item_string = re.sub('<[^<]+?>', '', item_string) # Eliminate HTML tags
        item_string = item_string.replace (' ', '') # Eliminate spaces
        item_string = item_string.replace (',', '') # Eliminate commas
        item_float = str_to_float (item_string)
        list_output.append (item_float)
        n = n + 1            
    return list_output

for symbol in list_symbol:
    line_cash = list_line_balance (symbol, "Cash & Short Term Investments")
    line_ppe = list_line_balance (symbol, "Property, Plant & Equipment - Gross")
    line_liab = list_line_balance (symbol, "Total Liabilities")
    line_ps = list_line_balance (symbol, "Preferred Stock (Carrying Value)")

    line_cfo = list_line_cashflow (symbol, "Net Operating Cash Flow")
    
    line_tax = list_line_income (symbol, "Income Tax")    

    #nshares = 

    # last year's PPE (at end of year) = PPE at the start of this year
    # this year's pre-tax free cash flow = This year's after-tax free cash flow + this year's income taxes
    # this year's after-tax free cash flow = this year's after-tax cash flow - this year's normalized capital spending
    # ASSUMPTION: this year's normalized capital spending = 10% of last year's PPE (at cost)
    # after-tax cash flow = official cash flow from operations
    # THUS:
    # this year's Dopeler earnings = this year's official cash flow from operations + this year's income taxes
    # - .1 * last year's PPE
    # this year's Dopeler Return On Equity = this year's Dopeler earnings / last year's PPE
    try:
        roe0 = (line_cfo [0] + line_tax [0] - .1 * line_ppe[1]) / line_ppe [1]
        roe1 = (line_cfo [1] + line_tax [1] - .1 * line_ppe[2]) / line_ppe [2]
        roe2 = (line_cfo [2] + line_tax [2] - .1 * line_ppe[3]) / line_ppe [3]
        roe_local = (roe0 + roe1 + roe2) / 3
    except:
        roe_local = None


    print symbol, roe_local
    # print "*****************"    
    # print line_cash
    # print line_ppe
    # print line_liab
    # print line_ps

    # print line_cfo

    # print line_tax
    # print "*****************"

