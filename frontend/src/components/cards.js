import "./cards.css";
import { query } from "../functions/queries";
import ReactStars from "react-rating-stars-component";
import {UserContext} from "../App";
import React from "react";


export function Card(props) {
    const [user, setUser] = React.useContext(UserContext);
    let style = `card border-primary mb-3 cards ${props?.style}`;
    function searchVideo(term,id,link=null) {
      props.videoSearch(term,id,link);
    }
    function changeStar(newRating) {
        console.log(props.song);
        if(props.song.play_count) {
            const q = `
            mutation updateSong($song:updateSong!){
                updateSong(song:$song) {
                  success,
                  errors,
                  song{
                    title,
                    play_count,
                    user_id
                  }
                }
              }
            `;
            query(q,{"song":{id:props.song.id,play_count:newRating}},user,(data)=>{
                console.log(data);
            })
        }
        else{
            const q = `
            mutation createSong($song:createSong!){
                createSong(song:$song){
                  success,
                  errors,
                  song{
                    id,
                    user_id,
                    song_id,
                    play_count,
                    title,
                    release,
                    artist_name,
                    year
                  }
                }
              }
            `;
            query(q,{"song": {
                "user_id":parseInt(user.id),
                "song_id":parseInt(props.song.song_id),
                "play_count":newRating,
                "title":props.song.title,
                "release":props.song.release,
                "artist_name":props.song.artist_name,
                "link":props.song.link,
                "year":props.song.year
            }},user,(data)=>{
                console.log(data);
                if(props.refresh){
                  props.refresh();
                }
            })

        }
    }
    return(
        <div className={style} onClick={()=>{searchVideo(`${props.title} ${props.header}`,props.song.id,props?.song?.link)}}>
            <div className="card-header">{props.header}</div>
            <div className="card-body text-dark">
                <h5 className="card-title">{props.title}</h5>
                <p className="card-text">{props.text}</p>
            </div>
            <div className="card-footer">
                <ReactStars 
                count ={5}
                size={24}
                value={props?.song?.play_count}
                activeColor="#ffd700"
                onChange={changeStar}
                />
            </div>
        </div>
    )
}