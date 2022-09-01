from re import search
from shutil import which
from bs4 import BeautifulSoup
import requests

def getRate(name ='The god father'): 
    '''
        Scrap the rate from the website : https://www.imdb.com
    '''
    # Request a searche url with the given name of the show
    r = requests.get('https://www.imdb.com/find?q='+name)

    soup = BeautifulSoup(r.content, 'html5lib')

    # Find the film and shows section of the result 
    a_tt = soup.find('a', attrs={'name':'tt'})
    if a_tt == None:
        return -1

    find_section = a_tt.parent.parent
    if find_section == None:
        return -1

    # Find the first result row 
    first_result = find_section.find('td', attrs={'class':'result_text'})
    if first_result == None:
        return -1
    
    a  = first_result.find('a')
    if a == None:
        return -1

    print('Rating for ', a.text)

    # Creating the url of the rating page 
    url = 'https://www.imdb.com' + a['href'] + 'ratings/'

    # Request the url created 
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    # Find the span that contain the rate. 
    rate = soup.find('span', attrs={'class':'ipl-rating-star__rating'})
    if rate == None:
        return -1

    return rate.text

if __name__ == "__main__":
    name = input('which rate du you search : ')
    print(getRate(name))