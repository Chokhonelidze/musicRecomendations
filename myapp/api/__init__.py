import os
from flask import Flask
from flask import send_file
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app,resources={r"/grapql/": {"origins": ["http://myhome.smho.site:3000/","localhost:5000","https://chokhonelidze.github.io"]}})


basedir = os.path.abspath(os.path.dirname(__file__))
"""
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
"""
"""
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'local',
    'host': 'localhost',
    'port': '5438',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
"""

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DB', "sqlite://")
app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG');
print(os.environ.get('DB', "sqlite://"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db,compare_type=True,include_schemas=True)


@app.route('/downloads/<path:filename>',methods=['GET'])
@cross_origin({"origins": ["http://myhome.smho.site:3000/","localhost:5000","https://chokhonelidze.github.io"]})
def downloadFile(filename):
    path = "/downloads/"+filename
    return send_file(path,as_attachment=True)