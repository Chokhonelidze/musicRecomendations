import React from "react";
import { UserContext } from "./App";
import { validator } from "./functions/validator";
import { query } from "./functions/queries";
import "./createSong.css";

export function CreateSong() {
    const [title,setTitle] = React.useState("");
    const [artist_name,setArtist_name] = React.useState("");
    const [link,setLink] = React.useState("");
    const [release,setRelease] = React.useState("");
    const [year,setYear] = React.useState("");
    const [user, setUser] = React.useContext(UserContext);
    const [showNewSong,setShowNew] = React.useState(false);
    const [errors,setErrors] = React.useState({});
    const [hasErrors,setHasErrors] = React.useState(false);


    function Form(props) {
        function sumbitSong() {
            try{
                validator(title,"name");
                validator(artist_name,"name");
                validator(link,"youtubeID");
                validator(release,"name");
                validator(year,"year");
                let allErrors = errors;
                allErrors['main'] = "";
                setHasErrors(false);
                const q =`
                mutation CreateNewSong($song:createPureSong){
                    createNewPureSong(song:$song){
                    success,
                    errors,
                    song{
                        song_id,
                        link,
                        title,
                        artist_name,
                        year,
                    }
                    }
                }
                `;
                query(q,{song:{
                    "title":title,
                    "artist_name":artist_name,
                    "link":link,
                    "release":release,
                    "year":year,
                }},user,(d)=>{
                    console.log(d);
                    if(d.pureSongResult.errors) {
                        let errs = d.pureSongResult.errors.join(" ");
                        setErrors(errs);
                        setHasErrors(true);
                    }
                    else {
                        setErrors({});
                        setHasErrors(false);
                    }
                })
            }
            catch(err) {
                let errs = errors;
                errs['artist_name'] = err;
                setErrors(errs);
                setHasErrors(true);
            }

        }
        return (<div className="formDisplay">
            <div className="card mb-3">
                <div className="card-header">
                    Create new Song 
                    <input type="button" value="❌" 
                    className="close_button"
                    onClick={()=>{setShowNew(false)}}
                    />
                </div>
                <div className="card-body">
                    SongTitle: <input type="text" 
                                value={title} 
                                name="title" 
                                className="form-control" 
                                onChange={(e)=>{
                                    try {
                                        setTitle(e.target.value);
                                        validator(title,"name");
                                        let err = errors;
                                        err['title'] = ""
                                        setErrors(err);
                                        setHasErrors(false);
                                    }
                                    catch(err){
                                        let errs = errors;
                                        errs['title'] = err.name;
                                        setErrors(errs);
                                        setHasErrors(true);
                                    }
                                }} />
                    Artist Name: <input type="text" 
                                value={artist_name} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{                           
                                    try {
                                        setArtist_name(e.target.value);
                                        validator(artist_name,"name");
                                        let err = errors;
                                        err['artist_name'] = ""
                                        setErrors(err);
                                        setHasErrors(false);
                                    }
                                    catch(err){
                                        let errs = errors;
                                        errs['artist_name'] = err.name;
                                        setErrors(errs);
                                        setHasErrors(true);
                                    }
                                }} />
                    Release: <input type="text" 
                                value={release} 
                                name="title" 
                                className="form-control" 
                                onChange={(e)=>{                                 
                                    try {
                                        setRelease(e.target.value);
                                        validator(release,"name");
                                        let err = errors;
                                        err['release'] = ""
                                        setErrors(err);
                                        setHasErrors(false);
                                    }
                                    catch(err){
                                        let errs = errors;
                                        errs['release'] = err.name;
                                        setErrors(errs);
                                        setHasErrors(true);
                                    }
                                }} />
                    Year: <input type="text" 
                                value={year} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{
                                    try {
                                        setYear(e.target.value);
                                        validator(year,"year");
                                        let err = errors;
                                        err['year'] = ""
                                        setErrors(err);
                                        setHasErrors(false);
                                    }
                                    catch(err){
                                        let errs = errors;
                                        errs['year'] = err.year;
                                        setErrors(errs);
                                        setHasErrors(true);
                                    }
                                }} />
                    Video ID: <input type="text" 
                                value={link} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{
                                    try {
                                        setLink(e.target.value);
                                        validator(link,"youtubeID");
                                        let err = errors;
                                        err['youtubeID'] = ""
                                        setErrors(err);
                                        setHasErrors(false);
                                    }
                                    catch(err){
                                        let errs = errors;
                                        errs['youtubeID'] = err.link;
                                        setErrors(errs);
                                        setHasErrors(true);
                                    }
                                }} />
                        <input type="submit" 
                        value="Create Song" 
                        className="btn btn-primary" 
                        onClick={sumbitSong}
                        />
                            
                </div>
            </div>

        </div>);
    }
    let view = "";
    if(user?.role === 1) {
        if(showNewSong) {
            view = <Form />
        }
        else {
            view = <input type="button" value="Add New Song" className="btn btn-primary" onClick={()=>{setShowNew(true)}} />
        }
    }
   return(<div>{view}</div>)

}