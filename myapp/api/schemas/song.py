type="""
type pureSong {
    song_id:ID!,
    title:String!,
    release:String,
    artist_name:String!,
    link:String,
    year:Int!
}

type pureSongsResult {
    success: Boolean!
    errors: [String]
    songs:[pureSong]
}
type pureSongResult {
    success: Boolean!
    errors: [String]
    song:pureSong
}
input createPureSong {
    title:String!,
    release:String,
    artist_name:String!,
    link:String,
    year:Int!
}
input pureSongFilters {
    search:String,
    filter:String! = "title",
    user:ID = ""
    limit:Int = 100,
    offset:Int = 0
}
"""
query="""
listPureSongs(filters:pureSongFilters!): pureSongsResult,
"""

mutation="""
createPureSong(song:createPureSong):pureSongResult
"""

pureSongs = {
    "type":type,
    "query":query,
    "mutation":mutation
}