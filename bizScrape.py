'''
Author: Felipe Zuniga Calier (Felipe-ZC)  

A python script that scrapes the HTML on search.sunbiz.org to determine if a
given business (in Florida) is an active business entity. 
'''

'''
TODO: Input validation!!!!

TODO: Add an option to retrieve inactive businesses.

TODO: Use mechanize to perform a deeper search, the most relevant results are
shown on the first page I'd like to give the user the option.

TODO: Add a verbose option, combine this with mechanize. If the verbose option 
is true, then the program will retrieve all active and/or inactive businesses
along with detailed information about the company. This detailed information
is found on sunbiz.

TODO: Add option to return data as python list.
'''

import re
import requests
import json
import argparse
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO, BytesIO

'''
DO NOT USE REGEX TO PARSE HTML!!!!
TODO: Find a way to parse HTML without using regex...
TODO: DISCUSS XML BOMBS WITH TEAM MEMBERS!
lmao
'''
def searchSunBiz(searchQuery):
    formattedInput = searchQuery.split(' ')
    formattedInput = list(map(lambda x: re.escape(x), formattedInput))
    formattedInput = r"|".join(formattedInput)

    # f strings are a new construct introduced in python 3.6, allows for string interpolation like in Node and other languages.
    link = f'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder={searchQuery.upper()}&searchTerm={searchQuery}'
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    parsedTags = soup.find_all('td')
    activeBusinesses = []
 
    '''
    Look for a match in each <td> element, if a match is found on index i then
    the <td> element that describes the business' status is found on index i +
    2. 

    This is a pretty basic approach to the problem but most of this is hacked
    af, needs review!
    '''
    # Find all active business entities...
    # TODO: Use variables for readability...
    # TODO: Decompose into functions...
    for index, tag in enumerate(parsedTags):
        #print(tag)
        if(tag.find('a')):
            textAsString = str(tag.find('a').string)
            matched = re.match(formattedInput, textAsString, re.I)
            if(matched):
                # TODO: CHECK FOR OUT OF BOUNDS YOU DICK!
                activeTag = parsedTags[index + 2]
                if(re.match('Active', str(activeTag.string))):
                    activeBusinesses.append(textAsString)
                    print('Active match found: ', textAsString)
                
            
    return activeBusinesses

'''
Return a list of results, let user
choose from list in frontend.
'''
def main(args):
    results = searchSunBiz(args.businessName)

    print(results)
    
    # Output results
    # if(args.json):
        # print(json.dumps({'data' : results}, sort_keys=True,
                        # indent=4, separators=(',', ': ')))
    # else:
        # print(f'Found {len(results)} active businesses while searching for {args.businessName}')
        # print("--------- Results ---------")
        # for result in results:
            # print(result)
    
    # # Return results in JSON or as a python list
    # return json.dumps({'data' : results}, sort_keys=True,
    #                    indent=None, separators=(',', ': '))

# Parse command line arguments and search sunbiz.org    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Searches for an active business entity on search.sunbiz.org by \'scraping\' the website.')
    parser.add_argument("businessName", help='The name of the business to search for.') 
    #parser.add_argument("-j", "--json",  help='Print results in JSON', action='store_true')
    args = parser.parse_args()
    main(args)
