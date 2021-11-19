# python -m pip install requests
# python -m pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup

base_url = ["https://mediawatch.dk", "https://itwatch.dk", "https://shippingwatch.dk", "https://finanswatch.dk", "https://medwatch.dk", "https://energiwatch.dk", "https://ejendomswatch.dk"]

media_topics = ["/Medienyt/Web/", "/Medienyt/TV/", "/Medienyt/Radio/", "/Medienyt/Aviser/", "/Medienyt/Ugeblade_magasiner/", "/Medienyt/Boeger/", "/Medienyt/politik/", "/Medienyt/tema/"]
it_topics = ["/ITNyt/Strategi/", "/ITNyt/Resultater/", "/ITNyt/Profiler/", "/ITNyt/Startup/", "/ITNyt/Politik/", "/ITNyt/M_and_A/", "/ITNyt/Brancher/"]
shipping_topics = ["/Rederier/", "/Virksomheder/", "/Offshore/", "/Havne/", "/logistik/", "/miljo_og_politik/"]
finans_topics = ["/Finansnyt/Pengeinstitutter/", "/Finansnyt/Forsikring/", "/Finansnyt/Pension/", "/Finansnyt/Realkredit/", "/Finansnyt/Fintech/", "/Finansnyt/Regulering/"]
med_topics = ["/Medicinal___Biotek/", "/Medico___Rehab/", "/laboratorie___diagnostik/", "/hoereapparater/"]
energi_topics = ["/Energinyt/Energiselskaber/", "/Energinyt/Olie___Gas/", "/Energinyt/Renewables/", "/Energinyt/Cleantech/", "/Energinyt/Politik___Markeder/"]
ejendom_topics = ["/Ejendomsnyt/Investorer/", "/Ejendomsnyt/Projektudvikling/", "/Ejendomsnyt/Almene_boliger/", "/Ejendomsnyt/Raadgivere/", "/Ejendomsnyt/service/", "/Ejendomsnyt/regulering/"]


topics_urls = [media_topics, it_topics, shipping_topics, finans_topics, med_topics, energi_topics, ejendom_topics]
page_num_url = "?pageNumber="


def scrape(number_of_pages=1):
    """
    This function goes through all websites listen in base_url, and the respective topic list.
    7 sites + 42 topics * 25 = 1225 articles per page

    :param number_of_pages:
    The number of pages to be looked through on each website
    """
    base_index = 0
    for base in base_url:
        for topic in topics_urls[base_index]:
            print("Søger i: " + base + topic)
            for i in range(int(number_of_pages)):
                content = []
                print("    Side: " + str(i+1))
                href_list = __get_hrefs(base + topic + page_num_url + str(i+1))
                if len(href_list) == 0:
                    print("list is empty")
                    break
                else:
                    for href in href_list:
                        content.append(__get_content(base, href))

                with open("ScrapeData.txt", 'a', encoding='utf-8') as f:
                    for c in content:
                        f.write(c.replace(" ", " "))
        base_index += 1


def __get_content(base,href):
    """
    Gets the content of the website "base" + "href", which is the actual article

    :param base:
    Page
    :param href:
    Sub page
    :return:
    The header of the page with the sub_header and the content
    """
    URL = base+href
    page = requests.get(URL)
    soup = BeautifulSoup(page.content.decode('utf-8'), "html.parser")

    article = soup.find_all("article")
    if len(article) == 0:
        return ""

    header: str = ""
    if len(article[0].find_all("h1")) != 0:
        header: str = article[0].find_all("h1")[0].text

    sub_header: str = ""
    if len(article[0].find_all("p", class_="c-lede")) != 0:
        sub_header: str = article[0].find_all("p", class_="c-lede")[0].text

    content: str = ""
    for e in article[0].find_all("div", class_="c-cms-content js-paywall"):
        content = content + e.text

    return header + sub_header + content


def __get_hrefs(URL):
    """
    Extracts the paths to articles from the topic site

    :param URL:
    The url to extract hrefs from
    :return:
    A list of hrefs
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("a", class_="c-thumbnail c-thumbnail--gutter")
    href_list = []
    for element in results:
        href_list.append(element['href'])

    return href_list
