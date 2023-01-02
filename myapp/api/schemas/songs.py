type="""
type song {
    id:ID!,
    user_id:Int!,
    song_id:Int!,
    play_count:Int,
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
type predictOutput {
    success: Boolean!,
    errors: [String],
    predict:[Int]
}
input songInput {
    user_id:Int!,
    song_id:Int!
}
input createSong{
    user_id:Int!,
    song_id:Int!,
    play_count:Int,
    title:String!,
    release:String,
    artist_name:String!,
    year:Int!
}
"""
query="""
    listSongs: songsResult,
    getSong(id:ID!) : songResult,
    predictSong(query:songInput!):predictOutput
"""
mutation="""
    createSong(song:createSong!):songResult
"""
songs = {
    "type":type,
    "query":query,
    "mutation":mutation
}