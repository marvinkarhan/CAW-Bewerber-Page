from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import shutil


def get_main_content_of_table(table):
    tr = table.find_elements_by_css_selector("tr")
    mainContent = {}
    for row in tr:
        content = row.find_elements_by_css_selector("td")
        if content and len(content) > 1:
            set_link_classes(content[1])
            mainContent[content[0].text] = content[1].get_attribute(
                "innerHTML")
    return mainContent


def get_next_steps(with_hochschulstart, edge_case=''):
    next_steps = '<div class="degree-next-steps"><h1 class="application-title">Nächste Schritte</h1><ol>'
    if with_hochschulstart:
        next_steps += '<li>Registrieren Sie sich bei <a href="https://dosv.hochschulstart.de" target="_blank" class="inline-link external-link">hochschulstart</a></li>'
    else:
        print(f'Application Edge Case: {edge_case}')
    next_steps += '<li>Registrieren Sie sich hier im <a href="https://c-campus.hs-mannheim.de/qisserver/pages/psv/selbstregistrierung/pub/selbstregistrierung.xhtml?_flowId=selfRegistrationRegister-flow&_flowExecutionKey=e1s1" class="inline-link external-link">Bewerbungs-Portal</a></li>'
    next_steps += '</ol></div>'
    return next_steps


def main_content_to_html(dict):
    html = '<table class="degree-information"><tbody>'
    next_steps = ''
    for th, td in dict.items():
        if 'Bewerbung' == th:
            if 'hochschulstart.de' in td:
                next_steps = get_next_steps(True)
            else:
                next_steps = get_next_steps(False, td)
        else:
            html += f'<tr><th>{th}</th><td>{td}</td></tr>'
    html += '</tbody></table>'
    return [html, next_steps]


def parse_contact_html(contact):
    set_link_classes(contact)
    # set class for phone spans
    phoneSpans = contact.find_elements_by_xpath(
        "//span[@class='u-icon--link-phone']")
    for phoneSpan in phoneSpans:
        driver.execute_script(
            "arguments[0].setAttribute('class','inline-telephone telephone')", phoneSpan) 
    galleries = contact.find_elements_by_class_name('ce-gallery')
    for gallery in galleries:
        gallery.set_attribute('outerHTML','')
    images = contact.find_elements_by_tag_name('img')
    for image in images:
        image.set_attribute('outerHTML', '')
    return f'<div class="degree-contact card">{contact.get_attribute("innerHTML")}</div>'


def set_link_classes(el):
    links = el.find_elements_by_css_selector('a')
    for link in links:
        classes = link.get_attribute("class")
        if 'mail' in classes:
            driver.execute_script(
                "arguments[0].setAttribute('class','inline-mail mail')", link)
            mailRef = link.text
            driver.execute_script(
                f"arguments[0].setAttribute('href','mailto:{mailRef}')", link)
        else:
            driver.execute_script(
                "arguments[0].setAttribute('class','inline-link external-link')", link)


def remove_illegal_tags(html: str) -> str:
    html = html.replace('<strong>', '<span class="bold-text">')
    html = html.replace('</strong>', '</span>')
    html = html.replace('<header>', '')
    html = html.replace('</header>', '')
    html = html.replace('_self', '_blank')
    html = html.replace('rel="external"', '')
    html = html.replace('_top', '_blank')
    html = html.replace('padding-left:10px;', '')
    html = html.replace('javascript:', '')
    return html


def parse_page_to_html(href):
    print(f'\nParsing {href} ...')
    driver.get(href)
    id = href.split('/')[-1].split('.')[0]
    html = f'<div id="{id}" class="application-main-content application-main-content-hidden">'
    headline = driver.find_element_by_css_selector('h1')
    html += f'<h1 class="application-title">{headline.text}</h1>'
    html += '<div class="degree-content-wrapper">'
    # get tabular degree information
    next_steps = ''
    try:
        tableContent = driver.find_element_by_css_selector("table")
        mainContent = get_main_content_of_table(tableContent)
        content_html, next_steps = main_content_to_html(mainContent)
        html += content_html
    except:
        print(f'No Table found in: {href}')
    # get contact information
    try:
        contacts = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/section/div/main/div[2]/div[2]/div/div/div')
        html += parse_contact_html(contacts)
    except:
        print(f'No Contact information for: {href} available!')
    html += f'</div>{next_steps}</div>'
    html = remove_illegal_tags(html)
    return html


def extract_german_degree_links():
    driver.get(
        'https://www.hs-mannheim.de/studieninteressierte/unsere-studiengaenge.html')
    return [element.get_attribute(
        "href") for element in driver.find_elements_by_xpath("//table//td/a")]


def extract_english_degree_links():
    # bachelor
    driver.get(
        'https://www.english.hs-mannheim.de/study-programmes/bachelor-courses.html')
    courses = [element.get_attribute("href") for element in driver.find_elements_by_xpath(
        '//main//li//a')]
    courses += [element.get_attribute("href") for element in driver.find_elements_by_xpath(
        '//main/div/div[3]/div/div/div//a')]
    # master
    driver.get(
        'https://www.english.hs-mannheim.de/study-programmes/master-courses.html')
    courses += [element.get_attribute("href") for element in driver.find_elements_by_xpath(
        '//main//li//a')]
    return courses


def create_folders():
    try:
        shutil.rmtree('./scraped_html')
    except OSprint as e:
        print("print: %s - %s." % (e.filename, e.strprint))
    os.mkdir('./scraped_html')
    os.mkdir('./scraped_html/german')
    os.mkdir('./scraped_html/german/bachelor')
    os.mkdir('./scraped_html/german/master')
    os.mkdir('./scraped_html/english')
    os.mkdir('./scraped_html/english/bachelor')
    os.mkdir('./scraped_html/english/master')


options = Options()
options.headless = True
options.add_argument('log-level=3')
driver = webdriver.Chrome('./chromedriver', options=options)


create_folders()
currentDir = os.getcwd()
# parse german degrees
for href in extract_german_degree_links():
    html = parse_page_to_html(href)
    if 'bachelorstudiengaenge' in href:
        os.chdir(currentDir + '\\scraped_html\\german\\bachelor')
    elif 'masterstudiengaenge' in href:
        os.chdir(currentDir + '\\scraped_html\\german\\master')
    else:
        print(f'No Categorization found for: {href} (no html created)')
        continue
    with open(f"{href.split('/').pop()}", "w", encoding='utf-8') as file:
        file.write(html)
# parse english degrees
for href in extract_english_degree_links():
    html = parse_page_to_html(href)
    if 'bachelor-courses' in href or 'bachelorstudiengaenge' in href:
        os.chdir(currentDir + '\\scraped_html\\english\\bachelor')
    elif 'master-courses' in href:
        os.chdir(currentDir + '\\scraped_html\\english\\master')
    else:
        print(f'No Categorization found for: {href} (no html created)')
        continue
    with open(f"{href.split('/').pop()}", "w", encoding='utf-8') as file:
        file.write(html)
