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
