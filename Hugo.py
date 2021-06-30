from requests_html import HTMLSession
import pandas as pd

s = HTMLSession()


def get_url(x):
  baseurl = 'https://www.genenames.org'
  url = f'https://www.genenames.org/tools/search/#!/?query=&rows=100&start={x}&filter=document_type:gene'
  r = s.get(url)
  r.html.render(timeout=40)
  urls = r.html.find('div.search-result')
  urllist = []
  for url in urls:
    links = baseurl + url.find('a', first=True).attrs['href']
    urllist.append(links)
  return urllist

def get_data(res):
  r = s.get(res)
  r.html.render(timeout=40)
  try:
    Approved_symbol = r.html.find('div.ng-binding.ng-scope', first=True).text
  except:
    Approved_symbol = ''
  try:
    Approved_name = r.html.find('div.ng-binding p', first=True).text
  except:
    Approved_name = ''
  try:
    UniProt = r.html.find('#report > div > protein-panel > div > div.panel-body > ext-res-panel-body > div > div > div.section.col-sm-12.col-xs-12.col-md-12 > div > div > a', first=True).text
  except:
    UniProt = ''

  dic = {
    'Approved_symbol': Approved_symbol,
    'Approved_name' : Approved_name,
    'UniProt' : UniProt
  }

  return dic

mainlist = []
for x in range(0, 443):
  links = get_url(x)
  for link in links:
    mainlist.append(get_data(link))

df = pd.DataFrame(mainlist)
df.to_csv('gene_data.csv', index=False)
print('fin')