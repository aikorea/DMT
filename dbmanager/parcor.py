from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

from mydb import initDB, findOne, findAll, insertDB
db = initDB()

@app.route('/')
def main_index():
    parcor = findOne(db)
    return "Hello World!</br></br>" + \
           "One sample parallel corpus</br>" + \
           parcor['en']+" = "+parcor['kr']

@app.route('/upload_one')
def upload_one():
    return render_template('upload_one_form.html')

@app.route('/upload_one', methods=['POST'])
def upload_one_post():
    entxt = request.form['en']
    krtxt = request.form['kr']
    src = request.form['src']
    result = insertDB(db, [{'en':entxt, 'kr':krtxt, 'src':src}])
    if result['success'] != 0:
        return 'Insertion failed'
    return "["+entxt+"], ["+krtxt+"] inserted!"

@app.route('/find_all')
def find_all():
    parcors = findAll(db)
    response = "<html>\n<body>\n<h1>Finding all parallel corpus!</h1></br></br>"
    response = response + "<table border=\"1\">\n" + \
                      "\t<tr><th>Index</th><th>English</th><th>Korean</th><th>Source</th></tr>\n"
    for parcor in parcors:
        response = response + "\t<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>"\
                            % (parcor['_id'], parcor['en'], parcor['kr'], parcor['src'])
    response = response + '</table>\n</body>\n</html>\n'
    return response

@app.route('/upload_file')
def upload_file():
    return render_template('upload_file_form.html')

@app.route('/upload_file', methods=['POST'])
def upload_file_post():
    corpus_file = request.files.get('textfile')
    src = request.form['src']
    parcors = []
    while True:
        kr = corpus_file.stream.readline()
        if not kr: break
        en = corpus_file.stream.readline()
        if not en: break
        kr = kr.strip()
        en = en.strip()
        parcors.append({'en':en, 'kr':kr, 'src':src})
    result = insertDB(db, parcors)
    if result['success'] != 0:
        return "Insertion failed"
    return "Uploaded "+corpus_file.filename+", %d rows inserted"%(len(result['ids']))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=1234)
