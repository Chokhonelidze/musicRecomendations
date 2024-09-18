import "./cards.css";
import { query } from "../functions/queries";
import { UserContext } from "../App";
import React from "react";
import { Rating } from 'react-simple-star-rating'
import { user_type } from "../functions/types";



export function Card(props:any) {

  const [user] = React.useContext(UserContext) as [user_type];

  const download = async (link:string) => {

        let headers = {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers":
            "Origin, X-Requested-With, Content-Type, Accept",
        };
        const server = process.env.REACT_APP_DOWNLOADSERVER;
        await fetch(server +link, {
          method: "GET",
          headers: headers,
        })
          .then((res) => res.blob())
          .then((blob) => {
            let a:HTMLElement = document.createElement("a");
            a.setAttribute('style',"display: none");
            document.body.appendChild(a);
            let file = window.URL.createObjectURL(blob);
            a.setAttribute("href",file);
            let name = String(link).split('/');
            a.setAttribute("download",props.title??"music")
            a.click();
            window.URL.revokeObjectURL(file);
          });
  

  };
  let style = `card border-primary mb-3 cards ${props?.style}`;
  function searchVideo(term:string, id:number, link:string = "",localLink:string="") {
    props.videoSearch(term, id, link,localLink);
  }
  function changeStar(newRating:number) {
    console.log(props.song);
    if (props.song.play_count) {
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
      query(
        q,
        { song: { id: props.song.id, play_count: newRating } },
        user,
        (data:string) => {
          console.log(data);
        }
      );
    } else {
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
      query(
        q,
        {
          song: {
            user_id: user.id as number,
            song_id: parseInt(props.song.song_id),
            play_count: newRating,
            title: props.song.title,
            release: props.song.release,
            artist_name: props.song.artist_name,
            link: props.song.local_link,
            year: props.song.year,
          },
        },
        user,
        (data:string) => {
          console.log(data);
        }
      ).then(() => {
        if (props?.refresh) {
          props.refresh();
        }
      });
    }
  }
  return (
    <div className={style}>
      <div className="card-header">{props.header}</div>
      <div
        className="card-body text-dark"
        style={{ cursor: "pointer" }}
        onClick={() => {
          searchVideo(
            `${props.title} ${props.header}`,
            props.song.song_id,
            props?.song?.link,
            props?.song?.local_link
          );
        }}
      >
        <h5 className="card-title">{props.title}</h5>
        <p className="card-text">{props.text}</p>
        {props?.predict ? (
          <h6>Predicted Star:{Number(props.predict).toFixed(2)}</h6>
        ) : (
          ""
        )}
      </div>
      <div className="card-footer">
      <Rating
          size={24}
          fillColor='gold'
          initialValue={props?.song?.play_count}
          onClick={changeStar}
        />
        {props?.song?.local_link ? (
          <button
            onClick={() => {
              download(props?.song?.local_link);
            }}
            style={{
              position:"relative",
              float:"right"
            }}
          >
            💾
          </button>
        ) : (
          ""
        )}
      </div>
    </div>
  );
}
