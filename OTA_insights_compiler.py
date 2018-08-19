#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  OTA_insights_compiler.py
#  
#  Copyright 2018 Paul <paul@Paul-jc>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""
This program is used to compile a large number of files that were downloaded from the site OTAinsights
(utilising seperate program) into a single CSV file for the purpose of running through a machine learning 
library. This is a subscriber only website that scrapes data from Online Travel Agent websites and combiles it daily. 
In order to obtain this data and in absence of an API a scraper was developed to dowload all files with pricing
history for any given day.

The format of the files had the date in poorly formatted form in cell A1. In order to make this easily computable 
for future purposes this program places the date beside each row of data, as well as week of year, day of week and 
month of year data for ease of future computing.

For use place the folder path as the file_folder variable
"""


import csv
import glob
import os
import itertools
import pandas as pd
from datetime import datetime

file_folder = '/home/user/Documents/OTA_Insights/'

files_to_convert = glob.glob(file_folder+'*.xlsx') # path to folder with data dump files

workings_folder = file_folder+'OTA_Insights_Workings/'

if not os.path.isdir(workings_folder):
    os.mkdir(workings_folder)


def read_csv(files): 
    iteration = 1 # In order to only write the title line to the file on the first iteration this will be incremented after each iteration
    # Read all excel files and convert to csv for future computing so that pandas library to read properly
    for excel in files:
        out = excel.split('.')[0]+'csv'
        df = pd.read_excel(excel)
        out = workings_folder+"temp_output.csv"
        df.to_csv(out)
        # Open the file just created in preperation for computing
        with open(out, 'r') as f:
            reader = csv.reader(f)
            reader = list(reader)
            date = reader[0][1] # date found in cell A1 in the sheet
            date = date[date.find(',')+2:len(date)-7]+date[len(date)-5:len(date)] # Date format was "Wednesday, January 5th 2018, this will extract the month, day and year removing the day of week and date suffix
            """Converts to computable format and then saves in various formats to write next to row."""
            date_data = datetime.strptime(date, '%B %d %Y')
            date_string = date_data.strftime('%d-%m-%Y')
            month_number = date_data.strftime('%m')
            year_number = date_data.strftime('%Y')
            weekday_number = date_data.weekday()
            week_number = datetime.date(date_data).isocalendar()[1]
            new_columns = [date_string,month_number,year_number,weekday_number,week_number]
            new_column_labels = ["date_string","month_number","year_number","weekday_number","week_number"]
            #Check if first iteration through the first file before writing the second row of the file which contains the labels to file
            if iteration == 1:
                """
                Takes line 2 of the file which contains the label. Adds the additional labels for the new columns created and writes it to a new file.
                New file created so that the folder can be used as a data dump file to collect new data over time but keep it all in one file for computing.
                """
                for row in itertools.islice(reader,1,2):
                    row.extend(new_column_labels) 
                    row = '/'.join(str(e) for e in row)
                    write_file = open(workings_folder+'output.csv', 'w')
                    write_file.write(row)
                    write_file.write("\n")
                    iteration += 1 #iterated after first line written so that it does not write again
            """
            For each row between rows 2 to 33 it will add the additional columns with the date information
            then write each row into the file created in the first iteration
            """
            for row in itertools.islice(reader,2,33):
                row.extend(new_columns)
                row = '/'.join(str(e) for e in row) # chose '/' as delimiter as some hotel names have commas in name, prefer to preserve this rather than stip all commas from names.
                write_file = open(workings_folder+'output.csv', 'a')
                write_file.write(row)
                write_file.write("\n")
        os.remove(workings_folder+"temp_output.csv") # Removes temporary file after each iteration
    print('File created')


read_csv(files_to_convert)
