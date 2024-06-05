from ..models import User
from ariadne import convert_kwargs_to_snake_case
from datetime import date 
from passlib.hash import sha256_crypt
from api import db
@convert_kwargs_to_snake_case
def test(obj,info)->str:
    return "test3"
@convert_kwargs_to_snake_case
def login(obj,info,query):
    email = query['email']
    password = query['password']
    print(email,password);
    user = User.query.filter_by(email=email).first()
    print(user)
    if user and sha256_crypt.verify(password, user.password):
        payload = {
            "success": True,
            "user":user.to_dict()
        }
    else:
        payload = {
            "success":False,
            "error":"Wrong user or Password"
        }
    return payload

@convert_kwargs_to_snake_case
def users_resolver(obj,info,query):
    limit = query["limit"]
    offset = query["offset"]
    search = False
    if query.get("search") != None:
        search = query["search"]
    id = False
    if query.get("id") != None:
        id = query["id"]
    try:
       users = []
       if id :
        users =  [User.query.filter_by(id=id).limit(limit).offset(offset).first()]
        print(users)
       elif search:
        users = [user.to_dict() for user in User.query.filter(User.email.like("%"+search+"%")).limit(limit).offset(offset).all()]
       else :
        users = [user.to_dict() for user in User.query.limit(limit).offset(offset).all()]
       payload = {
        "success": True,
        "users": users
       }
    except Exception as error:
        payload = {
            "success": False,
            "errors": error
        }
    return payload

queries = {"User":users_resolver,"login":login,"test":test}

@convert_kwargs_to_snake_case
def create_user_resolver(obj,info,user):
    try:
        today = date.today()
        userf = User.query.filter_by(email=user["email"]).first()
        if(userf):
            return {
                "success":False,
                "errors":["Email is already used"]
            }
        userI = User(
            email=user['email'],
            password=sha256_crypt.encrypt(user['password']),
            role=user['role'],
            created_at=today.strftime("%Y-%m-%d %H:%M:%S")
        )
        print(userI)
        db.session.add(userI)
        db.session.commit()
        payload = {
            "success": True,
            "user": userI.to_dict()
        }
    except ValueError:
         payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_user_resolver(obj,info,user):
    try:
        userI = User.query.get(user["id"])
        if userI:
            if user.get("email"):
                userI.email = user['email']
            if user.get("password"):
                userI.password = user['password']
            if(user.get("role")):
                userI.role = user['role']
        db.session.add(userI)
        db.session.commit()
        payload = {
            "success": True,
            "user": userI.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_user_resolver(obj,info,id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        payload = {"success": True, "user": user.to_dict()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload

"""
@convert_kwargs_to_snake_case
def encrypt_all_users(obj,info):
    try:
        users = User.query.all()
        for user in users:
            user.password = sha256_crypt.encrypt(user.password)
            db.session.add(user)
        db.session.commit()
        payload ={
            "success":True,
            "errors":[]
        }
    except Exception as error:
        payload ={
            "success":False,
            "errors": [str(error)]
        }
    return payload
"""

mutations = {
    "createUser":create_user_resolver,
    "updateUser":update_user_resolver,
    "deleteUser":delete_user_resolver
    }

User_resolver = {
    "queries":queries,
    "mutations":mutations
}
