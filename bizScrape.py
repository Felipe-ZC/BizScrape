import re
import requests

'''
For search.sunbiz.org

TODO: Match regex from user input to the link object's url field. 

TODO: Prep user input to match search.sunbiz.org's format. 

TODO: Make a request to search.sunbiz.org with user input, validate that the
user's input is a registered business entity in Florida.

TODO: Validate that company input is a registered business entity in Florida
and is active. 

TODO: Input validation!!!!

TODO: CLI (Command line interface)
'''

# Using requests
searchQuery = input('Search sunbiz.org: ')
formattedInput = searchQuery.upper()
#print(formattedInput)

# f strings are a new construct introduced in python 3.6, allows for string interpolation like in Node and other languages.
link = f'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder={searchQuery.upper()}&searchTerm={searchQuery}'
html = requests.get(link).text
#print('html: ', html)

'''
Use a regex to get all tr tags on the page (html).
Most of the anchor tags on the html page are the results to searchQuery, with some exceptions.
Using two flags:
    - M (multiline)
    - S makes the dot character (.) match any character including newlines.
'''

#tableRows = re.findall('\<tr\>.*\/tr\>', html, re.S)
tableRows = re.findall('\<td.*\>', html)
print(f'Found {len(tableRows)/3} results for {searchQuery}')

'''
Look for a match in each <td> element, if a match is found on index i
then the <td> element that describes the business' status is found on 
index i + 2. 

This is a pretty basic approach to the problem but most of this is hacked
af, needs review!
'''
print('searching for: ', searchQuery)
matches = [] # Holds all matches found, with their index...

for index, row in enumerate(tableRows):
    if(re.search(searchQuery, row, re.I)):
        print('Found a match for: ', searchQuery)
        # TODO: Check for out of bounds you dick!
        isActive = re.search('Active', tableRows[index + 2]);
        matches.append((row, isActive))

print(f'Matches found for {searchQuery}: {matches}')

'''
Return a list of results, let user
choose from list in frontend.
'''

    
