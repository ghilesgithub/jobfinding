from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import pprint
import requests
from bs4 import BeautifulSoup
import xlsxwriter 

app = Flask(__name__)

# Config DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        if request.form.get('titre')=='':
            job_searched = 'PMO'
        else:
            job_searched = request.form.get('titre')

        print(request.form)
    
        links=[]
        locations =[]
        title =[]
        summary = []

        result = requests.get("https://emplois.ca.indeed.com/emplois?as_and="+job_searched+"&as_phr=&as_any=Project+manager+chef+de+projet&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=Montr%C3%A9al%2C+QC&fromage=7&limit=20&sort=&psf=advsrch&from=advancedsearch")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')

        soup = soup.findAll("div", {"class": "jobsearch-SerpJobCard"})

        for sp in soup:

            a = sp.find("h2",{'class': 'title'}).find("a")
            link = a['href'] 

            sum_tmp = []
            summaries = sp.find("div", {"class": "summary"}).findAll('li')

            for sum in summaries:
                sum_tmp.append(sum.text)

            summary.append('\n'.join(sum_tmp))
            title.append(a.text)
            links.append(link)
            
            if sp.find('div',{'class':'location'}):
                locations.append(sp.find('div',{'class':'location'}).text)
            elif sp.find('span',{'class':'location'}):
                locations.append(sp.find('span',{'class':'location'}).text)
            else:
                locations.append('') 

        # i = 0

        # workbook = xlsxwriter.Workbook('hello.xlsx') 
        # worksheet = workbook.add_worksheet()

        # worksheet.write("A1", 'Titre')
        # worksheet.write("B1", 'Sommaire')
        # worksheet.write("C1", 'Endroit')
        # worksheet.write("D1", 'Lien')

        # for data in title:
        #     worksheet.write("A"+str(i+2), str(data))
        #     worksheet.write("B"+str(i+2), summary[i])
        #     worksheet.write("C"+str(i+2), locations[i])    
        #     worksheet.write("D"+str(i+2), 'https://ca.indeed.com'+ links[i] )
        #     i = i + 1

        # cell_format = workbook.add_format({'bg_color': 'white'})
        # worksheet.write('A1:AA250', '', cell_format)
        # worksheet.add_table('A1:D16') 

        # workbook.close()

        return render_template('features.html',locations=locations,title=title,summary=summary,links=links)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
