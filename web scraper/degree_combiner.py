import os
import shutil

COMBINED_HTML = './combined_html'
BACHELOR_GERMAN = './scraped_html/german/bachelor'
BACHELOR_ENGLISH = './scraped_html/english/bachelor'
MASTER_GERMAN = './scraped_html/german/master'
MASTER_ENGLISH = './scraped_html/english/master'
SIDEBAR_GERMAN_BACHELOR = '../portlets/sidebars/german/sidebar_detail_bachelor.html'
SIDEBAR_ENGLISH_BACHELOR = '../portlets/sidebars/english/sidebar_detail_bachelor.html'
SIDEBAR_GERMAN_MASTER = '../portlets/sidebars/german/sidebar_detail_master.html'
SIDEBAR_ENGLISH_MASTER = '../portlets/sidebars/english/sidebar_detail_master.html'
def create_folder():
    try:
        shutil.rmtree(COMBINED_HTML)
    except shutil.Error as e:
        print("print: %s - %s." % (e.filename, e.strprint))
    os.mkdir(COMBINED_HTML)

def create_file(directory: str, name: str, sidebar: str):
    information = '<div class="application-wrapper">'
    for filename in os.listdir(directory):
        with open(directory + '/' + filename, 'r') as file:
            information += file.read()
    with open(sidebar, 'r') as file:
        information += file.read()
    information += '</div>'
    with open(COMBINED_HTML + '/' + name + '.html', 'w') as file:
        file.write(information)




#Start
create_folder()
create_file(BACHELOR_GERMAN, 'bachelor_german', SIDEBAR_GERMAN_BACHELOR)
create_file(BACHELOR_ENGLISH, 'bachelor_english', SIDEBAR_ENGLISH_BACHELOR)
create_file(MASTER_GERMAN, 'master_german', SIDEBAR_GERMAN_MASTER)
create_file(MASTER_ENGLISH, 'master_english', SIDEBAR_ENGLISH_MASTER)