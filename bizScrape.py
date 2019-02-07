import re
import requests

'''
For search.sunbiz.org

TODO: Input validation!!!!

TODO: CLI (Command line interface)

TODO: Encapsulate code into module or whatever python uses
to package and prepare for depolyment.
'''

'''
Use a regex to get all tr tags on the page (html).
Most of the anchor tags on the html page are the results to searchQuery, with some exceptions.
Using two flags:
    - M (multiline)
    - S makes the dot character (.) match any character including newlines.
'''
def searchSunBiz(searchQuery):
    formattedInput = searchQuery.split(' ')
    formattedInput = list(map(lambda x: re.escape(x), formattedInput))
    formattedInput = r"|".join(formattedInput)

    # f strings are a new construct introduced in python 3.6, allows for string interpolation like in Node and other languages.
    link = f'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder={searchQuery.upper()}&searchTerm={searchQuery}'
    html = requests.get(link).text
    tableRows = re.findall('\<td.*', html)

    '''
    Look for a match in each <td> element, if a match is found on index i
    then the <td> element that describes the business' status is found on 
    index i + 2. 

    This is a pretty basic approach to the problem but most of this is hacked
    af, needs review!
    '''
    parsed = [] # Holds all matches found, with their index...

    for index, row in enumerate(tableRows):
        if(re.search(formattedInput, row, re.I)):
             # TODO: Check for out of bounds you dick!
            isActive = re.search('Active', tableRows[index + 2]);
            companyName = re.search('\>[a-zA-Z0-9., ]+\<', row)
            # Collect active businesses
            if(companyName and isActive):
                formattedName = re.sub('<|>', '', companyName.group(0))
                parsed.append(formattedName)

    return parsed

'''
Return a list of results, let user
choose from list in frontend.
'''
#TODO: Return resulting list as JSON!!!!! (Come on bro...)
def main():
    searchQuery = input('Search sunbiz.org: ')
    result = searchSunBiz(searchQuery)

    print(f'Found {len(result)} active businesses registered while searching for {searchQuery}')
    print(result)

    return result;

if __name__ == '__main__':
    main()
