type="""
type song {
    id:ID!,
    user_id:Int!,
    song_id:Int!,
    pley_cout:Int,
    title:String!,
    release:String,
    artist_name:String!,
    year:Int!
}
type songsResult {
    success: Boolean!
    errors: [String]
    songs:[song]
}
type songResult {
    success: Boolean!
    errors: [String]
    song:song
}
"""
query="""
    listSongs: songsResul
    getSong(id:ID!) : songResult
"""
mutation="""
"""
songs = {
    "type":type,
    "query":query,
    "mutation":mutation
}