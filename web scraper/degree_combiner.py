import os
import shutil

COMBINED_HTML = './combined_html'
BACHELOR_GERMAN = './scraped_html/german/bachelor'
SIDEBAR_BACHELOR = '../portlets/sidebars/sidebar_detail_bachelor.html'
SIDEBAR_MASTER = '../portlets/sidebars/sidebar_detail_master.html'
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
create_file(BACHELOR_GERMAN, 'bachelor_german', SIDEBAR_BACHELOR)