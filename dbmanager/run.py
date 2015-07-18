from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

from lib.mydb import initDB, findOne, findAll, insertDB
db = initDB()

@app.route('/')
def main_index():
    parcor = findOne(db)
    return "Hello World!</br></br>" + \
           "One sample parallel corpus</br>" + \
           parcor['data1']+" = "+parcor['data2']

@app.route('/upload_one')
def upload_one():
    return render_template('upload_one_form.html')

@app.route('/upload_one', methods=['POST'])
def upload_one_post():
    result = insertDB(db, [request.form])
    if result['success'] != 0:
        return 'Insertion failed'
    return "["+request.form['data1']+"], ["+request.form['data2']+"] inserted!"

@app.route('/find_all')
def find_all():
    parcors = findAll(db)
    response = "<html>\n<body>\n<h1>Finding all parallel corpus!</h1></br></br>"
    response = response + "<table border=\"1\">\n" + \
                      "\t<tr><th>Index</th><th>Lang 1</th><th>Lang 2</th><th>Source</th></tr>\n"
    for parcor in parcors:
        response = response + "\t<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>"\
                            % (parcor['_id'], parcor['data1'], parcor['data2'], parcor['src'])
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
        data2 = corpus_file.stream.readline()
        if not data2: break
        data1 = corpus_file.stream.readline()
        if not data1: break
        data1 = data1.strip()
        data2 = data2.strip()
        parcors.append({'data1':data1, 'data2':data2, 'lang1':'en', 'lang2':'kr', 'src':src})
    result = insertDB(db, parcors)
    if result['success'] != 0:
        return "Insertion failed"
    return "Uploaded "+corpus_file.filename+", %d rows inserted"%(len(result['ids']))

import sys
if __name__ == '__main__':
    app.debug = True
    host = '0.0.0.0'
    port = 5000
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
    app.run(host=host, port=port)
