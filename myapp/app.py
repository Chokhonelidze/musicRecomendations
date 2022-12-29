from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import listPosts_resolver, getPost_resolver
from api.mutations import create_post_resolver,update_post_resolver,delete_post_resolver
from api.schemas.posts import type,query,mutation
from api.resolvers.posts import queries,mutations 
posts = {
    "type":type,
    "query":query,
    "mutation":mutation,
    "query_resolver":queries,
    "mutations_resolver":mutations
}
print(posts["type"])
type_defs = ""
type=[]
query=[]
mutation=[]
objs = [posts]

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





type_defs = "\n".join(type)+"\n"+"type Query { \n"+"/n".join(query)+"} \n type Mutation {"+"\n".join(mutation)+"\n }"


#query_resolver.set_field("listPosts", listPosts_resolver)
#query_resolver.set_field("getPost", getPost_resolver)
#mutation_resolver.set_field("createPost", create_post_resolver)
#mutation_resolver.set_field("updatePost",update_post_resolver)
#mutation_resolver.set_field("deletePost", delete_post_resolver)
#type_defs = load_schema_from_path("schema.graphql")

schema = make_executable_schema(
    type_defs,query_resolver,mutation_resolver, snake_case_fallback_resolvers
)
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
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