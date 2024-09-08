
/**
 * users types
 */
export type user_type = {
    id:number,
    email:string,
    role:number,
    created_at:string,
  }
 
export type createUserResult_type = {
  createUser:{
    success: boolean,
    errors: [string],
    user: user_type
  }
}
export type loginOutput_type = { 
  login:{
    success: boolean,
    error: string,
    user:user_type
  }
}
/**
 * song
 */
export type pureSong_type = {
  song_id:number,
  title:string,
  release:string,
  artist_name:string,
  link:string,
  year:number,
  predict:string,
  common:boolean
}
export type pureSongsResult_type = {
  listPureSongs:{
  success: boolean
  errors: [string]
  songs:[pureSong_type]
  }
}
/**
 * songs
 */
export type song_type = {
  id:number,
  user_id:number,
  song_id:number,
  play_count:number,
  title:number,
  release:string,
  artist_name:number,
  local_link:string,
  year:number,
}
export type songsResult_type = {
  listSongs:{
    success: boolean,
    errors: [string],
    songs:[song_type]
  }
}
export type getSong_type = {
  getSong :{
    success: boolean,
    errors: [string],
    song:pureSong_type
  }
}
export type predictOutput_type = {
  predictSong:{
    success: boolean,
    errors: [string],
    predict:[prediction_type]
  }
}
export type prediction_type = {
  id:number,
  score:string,
  predict:string,
  common:boolean,
}