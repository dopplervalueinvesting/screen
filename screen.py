#! /usr/bin/python

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
# Output: 1-D data list
def col_title (list_input, string_input):
    col_num_local = col_num_title (list_input, string_input)
    list_output = column_data (list_input, col_num_local) 
    return list_output

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
    # Output: 1-D data list containing all stock symbols
    def column_all (self, string_input):
        list_input = self.data ()
        list_titles_local = list_titles (list_input)
        num_col_symbol = col_num_title (list_input, string_input)
        list_output = column_data (list_input, num_col_symbol)
        return list_output
        
    # Purpose: get a list of the symbols for all of the stocks profiled
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list containing all stock symbols
    def symbol_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'Symbol')
        return list_output

    # Purpose: get a list of the sectors for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list containing the sectors for each stock
    def sector_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'Sector')
        return list_output

    # Purpose: get a list of the industries for each stock
    # Input: 2-D data list containing all information in the file
    # Output: 1-D data list containing the industry for each stock
    def industry_all (self):
        list1 = self.data ()
        list_output = col_title (list1, 'industry')
        return list_output

    # Purpose: get a list of stock symbols that are NOT funds
    # Inputs: 1-D data lists containing the sector and industry information
    # Output: 1-D data list consisting of selected stock symbols
    def symbol_selected (self):
        list1 = self.sector_all ()
        list2 = self.industry_all ()
        list3 = self.symbol_all ()
        list_output = []
        n_length = len (list3)
        n_last = n_length -1
        n = 0
        while n <= n_last:
            if (list1 [n] <> "n/a" ) & (list2 [n] <> "n/a" ):
                string_symbol = list3 [n]
                string_symbol = string_symbol.replace (' ', '') # Eliminate spaces
                string_symbol = string_symbol.replace ('^', '') # Eliminate '^' symbol
                string_symbol = string_symbol.replace ('/', '-') # Replace the '/' symbol due to filename issues
                # Note that all symbols in which the '^' symbol is not at the end belong to funds (screened out)
                list_output.append (string_symbol)
            n = n + 1
        return list_output

#######################################################################################################################
# PART 2: Using Exchange.symbol_selected, compile the list of ticker symbols from the AMEX, NYSE, and NASDAQ exchanges.
#######################################################################################################################

# Exchange_amex = Exchange ('amex')
# Exchange_nyse = Exchange ('nyse')
# Exchange_nasdaq = Exchange ('nasdaq')
Exchange_test = Exchange ('test')
# list_amex = Exchange_amex.symbol_selected ()
# list_nyse = Exchange_nyse.symbol_selected ()
# list_nasdaq = Exchange_nasdaq.symbol_selected ()
list_test = Exchange_test.symbol_selected ()
list_symbols = []
# for item in list_amex:
    # list_symbols.append (item)
# for item in list_nyse:
    # list_symbols.append (item)
# for item in list_nasdaq:
    # list_symbols.append (item)
for item in list_test:
    list_symbols.append (item)

num_stocks = len (list_symbols)

############################################################
# PART 3: For each stock, download the financial data needed
############################################################
# NOTE: Downloading is bypassed if the file to be replaced is less than 4 days old.  
# NOTE: Delay is used to avoid overwhelming the servers.

# Getting profile information from Yahoo
# Getting financial figures from CNBC (more data than Yahoo, capable of handling big loads)
URL_BASE_YAHOO = 'http://finance.yahoo.com/q/'
URL_BASE_SMARTMONEY = 'http://www.smartmoney.com/quote/'
LOCAL_BASE = dir_doppler + '/screen-downloads'

# Yahoo Finance URL for profile data
def url_profile (symbol1):
    url1 = URL_BASE_YAHOO + 'pr?s=' + symbol1 + '+Profile'
    return url1

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

def local_profile (symbol1):
    url1 = local_root (symbol1) + '/profile.html'
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
    url1 = url_profile (symbol1)
    url2 = url_balancesheet (symbol1)
    url3 = url_income (symbol1)
    url4 = url_cashflow (symbol1)
    local1 = local_profile (symbol1)
    local2 = local_balancesheet (symbol1)
    local3 = local_income (symbol1)
    local4 = local_cashflow (symbol1)    

    print "Downloading data on " + symbol1

    # Download profile information
    url = url1
    file_name = local1
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading profile data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .9)) # Delay
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"

    # Download balance sheet information
    url = url2
    file_name = local2
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading balance sheet data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .9))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"

    # Download income information
    url = url3
    file_name = local3
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading income statement data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .9))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"

    # Download cash flow information
    url = url4
    file_name = local4
    file_age = age_of_file (file_name)
    if file_age > 3:
        try:
            print "Downloading cash flow data"
            f = urlopen (url)
            local_file = open (file_name, 'w') # Open local file
            local_file.write (f.read())
            local_file.close ()
            time.sleep (random.uniform (.1, .9))
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
    else:
        print "Local file is less than 4 days old - skipping download"
    
create_dir (LOCAL_BASE) # Create screen-downloads directory if it does not already exist
i_stock = 0
i_stock_max = len (list_symbols)
for symbol in list_symbols:
    create_dir (local_root (symbol)) # Create directory for stock if it does not already exist
    download_data (symbol)
    i_stock = i_stock + 1
    print "Download completion: " + str(i_stock) + '/' + str(i_stock_max)
    
###############################################################
# PART 4: For each stock, process the financial data downloaded
###############################################################

# Purpose: Obtain data for a specific line item
# Inputs: two strings (one of the symbol, one for the title of the line item)
# Output: list of numbers for the line item
def list_line (symbol_input, title_input):
    url_local = local_balancesheet (symbol_input)
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
        try:
            item_float = float (item_string)
        except:
            item_float = None
        list_output.append (item_float)
        n = n + 1            
    return list_output

for symbol in list_symbols:
    line_cash = list_line (symbol, "Cash & Short Term Investments")

    print "*****************"    
    print line_cash
    print "*****************"

