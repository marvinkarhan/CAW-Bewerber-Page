from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome('./chromedriver', options=options)

driver.get(
    'https://www.hs-mannheim.de/studieninteressierte/unsere-studiengaenge.html')


def get_main_content_of_table(table):
    tr = table.find_elements_by_css_selector("tr")
    mainContent = {}
    for row in tr:
        content = row.find_elements_by_css_selector("td")
        if content and len(content) > 1:
            mainContent[content[0].text] = content[1].text
    return mainContent


def main_content_to_html(dict):
    html = '<table class="degree-information"><tbody>'
    for th, td in dict.items():
        html += f'<tr><th>{th}</th><td>{td}</td></tr>'
    html += '</tbody></table>'
    return html


def parse_contact_html(contact):
    # transform classes of links
    links = contact.find_elements_by_css_selector('a')
    for link in links:
        classes = link.get_attribute("class")
        if 'mail' in classes:
            driver.execute_script(
                "arguments[0].setAttribute('class','mail')", link)
            mailRef = link.text
            driver.execute_script(
                f"arguments[0].setAttribute('href','mailto:{mailRef}')", link)
        else:
            driver.execute_script(
                "arguments[0].setAttribute('class','external-link')", link)
    # set class for phone spans
    phoneSpans = contact.find_elements_by_xpath(
        "//span[@class='u-icon--link-phone']")
    for phoneSpan in phoneSpans:
        driver.execute_script(
            "arguments[0].setAttribute('class','telephone')", phoneSpan)
    return contact.get_attribute('innerHTML')


def get_sidebar():
    return '<div class="application-sidebar">    <h1 class="application-title">Nützliche Links</h1>    <ul class="list-links">      <li><a class="link-text" target="_blank" href="https://www.hs-mannheim.de/bewerbung/vorbereitungskurse.html">Vorbereitungskurse</a></li>      <li><a class="link-text" target="_blank" href="https://www.hs-mannheim.de/bewerbung/nc-werte.html">NC-Werte</a></li>      <li><a class="link-text" target="_blank" href="https://www.hs-mannheim.de/bewerbung/bewerbungsunterlagen.html">Bewerbungsunterlagen</a></li>      <li><a class="link-text" target="_blank" href="https://www.hs-mannheim.de/bewerbung/zulassungsvoraussetzungen.html">Zulassungsvorraussetzungen</a></li>    </ul>    <div class="sidebar-steps">      <a href="https://c-campus.hs-mannheim.de/qisserver/pages/cs/sys/portal/linkedPortlet.faces?portletGuid=88fde149-9fce-4dcc-8cee-8a5a8207bea7&sig=3344a8ffbff58348d1d26b591057b03b" class="sidebar-step-item">        <div class="sidebar-step-item-circle active">1</div>        <div class="sidebar-step-item-text active">Abschluss wählen</div>      </a>      <div class="sidebar-line active"></div>      <a href="https://c-campus.hs-mannheim.de/qisserver/pages/cs/sys/portal/linkedPortlet.faces?portletGuid=cec79cdb-38fd-43fc-8dac-8f33bec6cc01&sig=c8d5461e8b3562b6da1091e7e3b60412" class="sidebar-step-item">        <div class="sidebar-step-item-circle active">2</div>        <div class="sidebar-step-item-text active">Studiengang auswählen</div>      </a>      <div class="sidebar-line active"></div>      <a href="" class="sidebar-step-item">        <div class="sidebar-step-item-circle active">3</div>        <div class="sidebar-step-item-text active">Bewerbung durchführen</div>      </a>    </div>    <div class="sidebar-contact">      <div class="sidebar-contact-header small-text">Kontakt</div>      <div class="sidebar-contact-address">        <div class="small-text">Hochschule Mannheim</div>        <div class="small-text">Paul-Wittsack-Straße 10</div>        <div class="small-text">68163 Mannheim</div>      </div>      <ul class="sidebar-contact-communication">        <li class="sidebar-contact-communication-item telephone">          <a href="tel:" class="small-text">+49 621 292-6111</a>        </li>        <li class="sidebar-contact-communication-item small-text mail">          <a href="mailto:studium@hs-mannheim.de" class="regular-text">studium@hs-mannheim.de</a>        </li>      </ul>    </div>  </div>'


hrefs = [element.get_attribute(
    "href") for element in driver.find_elements_by_xpath("//table//td/a")]

for href in [hrefs.pop()]:
    print(href)
    # navigate to degree
    driver.get(href)
    # set html wrapper
    html = '<div class="application-wrapper"><div class="application-main-content">'
    # set headline
    headline = driver.find_element_by_css_selector('h1')
    html += f'<h1 class="application-title">{headline.text}</h1>'
    # extract content
    # get tabular degree information
    tableContent = driver.find_element_by_css_selector("table")
    if tableContent:
        mainContent = get_main_content_of_table(tableContent)
        html += main_content_to_html(mainContent)
    # extract contact
    # get content by xpath
    contacts = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/section/div/main/div[2]/div[2]/div/div/div')
    if contacts:
        html += parse_contact_html(contacts)
    # close main content
    html += '</div>'
    # add sidebar
    html += get_sidebar()
    # close doc
    html += '</div>'
    print(html)
