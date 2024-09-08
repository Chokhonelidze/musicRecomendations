from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.schemas.posts import posts
from api.resolvers.posts import posts_resolver
from api.schemas.users import users
from api.resolvers.users import User_resolver
from api.schemas.songs import songs
from api.resolvers.songs import songs_resolver
from api.schemas.song import pureSongs
from api.resolvers.song import pure_songs_resolver
from flask_cors import cross_origin
#from surprise.prediction_algorithms.knns import KNNBasic

#gs_optimized = KNNBasic(sim_options={'name':'pearson_baseline','user_based': True}, k=30, min_k=9, verbose=False)
#gs_optimized.fit(data)
#gs_optimized.predict(6958,1671,verbose=True)

posts = {
    "type":posts["type"],
    "query":posts["query"],
    "mutation":posts["mutation"],
    "query_resolver":posts_resolver["queries"],
    "mutations_resolver":posts_resolver["mutations"]
}
users = {
    "type":users["type"],
    "query":users["query"],
    "mutation":users["mutation"],
    "query_resolver":User_resolver["queries"],
    "mutations_resolver":User_resolver["mutations"]
}
song = {
    "type":pureSongs["type"],
    "query":pureSongs["query"],
    "mutation":pureSongs["mutation"],
    "query_resolver":pure_songs_resolver["queries"],
    "mutations_resolver":pure_songs_resolver["mutations"]
}
songs = {
    "type":songs["type"],
    "query":songs["query"],
    "mutation":songs["mutation"],
    "query_resolver":songs_resolver["queries"],
    "mutations_resolver":songs_resolver["mutations"]
}

type_defs = ""
type=[]
query=[]
mutation=[]
objs = [posts,users,songs,song]

query_resolver = ObjectType("Query")

mutation_resolver = ObjectType("Mutation")
for ob in objs:
    type.append(ob["type"])
    query.append(ob["query"])
    mutation.append(ob["mutation"])
    for item in ob["query_resolver"]:
        query_resolver.set_field(item,ob["query_resolver"][item])
    for item in ob["mutations_resolver"]:
        mutation_resolver.set_field(item,ob["mutations_resolver"][item])





type_defs = "\n".join(type)+"\n"+"type Query { \n"+"\n".join(query)+"} \n type Mutation {"+"\n".join(mutation)+"\n }"



schema = make_executable_schema(
    type_defs,query_resolver,mutation_resolver, snake_case_fallback_resolvers
)
@app.route("/graphql", methods=["GET"])
@cross_origin()
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
@cross_origin()
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code



