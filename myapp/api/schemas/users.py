type = """
type User {
    id:ID!,
    email:String!,
    password:String!,
    role:Int!,
    created_at:String!,
}
type UsersResult {
    success: Boolean!
    errors: [String]
    users: [User]
}
type UserResult {
    success: Boolean!
    errors: [String]
    user: User
}
type loginOutput {
    success: Boolean!,
    error: String,
    user:User
}
input createUser {
    email:String!,
    password:String!
    role:Int
}
input updateUser {
    id:ID!,
    email:String,
    password:String,
    role:Int
}
input UsersQuery {
    limit: Int = 100,
    offset: Int = 0,
    search: String,
    id:ID
}
input loginInput {
    email: String!,
    password: String!
}
"""
query = """
User(query:UsersQuery):UsersResult,
login(query:loginInput):loginOutput
"""
mutation = """
createUser(user:createUser!):UserResult,
deleteUser(id:ID!):UserResult,
updateUser(user:updateUser):UserResult
"""

users = {
    "type":type,
    "query":query,
    "mutation":mutation
}