import os,torch,whisper
from flask import Flask
from flask import send_file
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_executor import Executor

torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
translate = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)
executor = Executor(app)
CORS(app,resources={r"/graphql/": {"origins": ["http://myhome.smho.site:3000/","localhost:5000","http://localhost:3000","https://chokhonelidze.github.io","http://209.122.34.37:3000","http://209.122.34.37:3000/"]}})


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
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_MAX_WORKERS'] = 5
print(os.environ.get('DB', "sqlite://"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db,compare_type=True,include_schemas=True)


@app.route('/downloads/<path:filename>',methods=['GET'])
@cross_origin({"origins": ["http://myhome.smho.site:3000/","http://localhost:3000","localhost:5000","https://chokhonelidze.github.io","http://209.122.34.37:3000","http://209.122.34.37:3000/"]})
def downloadFile(filename):
    path = "/downloads/"+filename
    return send_file(path,as_attachment=True)