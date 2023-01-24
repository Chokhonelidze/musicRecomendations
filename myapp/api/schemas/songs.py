type="""
type song {
    id:ID!,
    user_id:Int!,
    song_id:Int!,
    play_count:Int,
    title:String!,
    release:String,
    artist_name:String!,
    link:String,
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
type prediction {
    id:ID,
    score:String,
    common:Boolean,
}
type predictOutput {
    success: Boolean!,
    errors: [String],
    predict:[prediction]
}
type updateAllSongsType {
    success: Boolean!,
    errors:[String],
    ids:[Int]
}
input songInput {
    user_id:Int!,
}
input songFilters {
    search:String,
    filter:String! = "title",
    user:ID = ""
    limit:Int = 100,
    offset:Int = 0
}
input createSong{
    user_id:Int!,
    song_id:Int!,
    play_count:Int,
    title:String!,
    release:String,
    artist_name:String!,
    link:String,
    year:Int!
}
input updateSong{
    id:ID,
    play_count:Int,
    title:String,
    release:String,
    artist_name:String,
    link:String,
    year:Int
}
input updateAllSongLinksInput {
    id:ID!,
    link:String!
}
"""
query="""
    listSongs(filters:songFilters!): songsResult,
    getSong(id:ID!) : songResult,
    predictSong(query:songInput!):predictOutput
"""
mutation="""
    createSong(song:createSong!):songResult,
    updateSong(song:updateSong!):songResult,
    updateAllSongLinks(song:updateAllSongLinksInput):updateAllSongsType
"""
songs = {
    "type":type,
    "query":query,
    "mutation":mutation
}