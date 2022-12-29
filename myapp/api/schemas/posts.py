type = """
type Post {
    id: ID!
    title: String!
    description: String!
    created_at: String!
}

type PostResult {
    success: Boolean!
    errors: [String]
    post: Post
}

type PostsResult {
    success: Boolean!
    errors: [String]
    posts: [Post]
}
"""
query = """
listPosts: PostsResult!
getPost(id: ID!): PostResult!
""";
mutation = """
createPost(title: String!, description: String!, created_at: String): PostResult!
updatePost(id: ID!, title: String, description: String): PostResult!
deletePost(id: ID): PostResult!
"""
