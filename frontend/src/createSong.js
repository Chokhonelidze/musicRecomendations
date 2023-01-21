import React from "react";
import { UserContext } from "./App";
import { validator } from "./functions/validator";
import { query } from "./functions/queries";
import "./createSong.css";

export function CreateSong() {

    const [user, setUser] = React.useContext(UserContext);
    const [showNewSong,setShowNew] = React.useState(false);

    function Form() {
        const [title,setTitle] = React.useState("");
        const [artist_name,setArtist_name] = React.useState("");
        const [link,setLink] = React.useState("");
        const [release,setRelease] = React.useState("");
        const [year,setYear] = React.useState("");
        const [errors,setErrors] = React.useState({});
        const [hasErrors,setHasErrors] = React.useState(false);
        function sumbitSong() {
            try{
                /*
                validator(title,"name");
                validator(artist_name,"name");
                validator(link,"youtubeID");
                validator(release,"name");
                validator(year,"year");
                */
                console.log("success")
                let allErrors = errors;
                allErrors['main'] = "";
                setErrors(allErrors);
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
                    "link":`//www.youtube.com/embed/${link}?autoplay=1&mute=0`,
                    "release":release,
                    "year":parseInt(year),
                }},user,(d)=>{
                    console.log(d);
                    if(d.createNewPureSong?.errors) {
                        let errs = d.createNewPureSong.errors.join(" ");
                        let allErrs = errors;
                        allErrs["main"] = errs;
                        setErrors(allErrs);
                        setHasErrors(true);        
                    }
                    else {
                        setErrors({});
                        setHasErrors(false);
                        setShowNew(false);
                    }
                })
            }
            catch(err) {
                console.log(err);
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
                                        validator(e.target.value,"name");
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
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["title"]}</> : ""}
                                </h5>
                    Artist Name: <input type="text" 
                                value={artist_name} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{                           
                                    try {
                                        setArtist_name(e.target.value);
                                        validator(e.target.value,"name");
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
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["artist_name"]}</> : ""}
                                </h5>
                    Release: <input type="text" 
                                value={release} 
                                name="release" 
                                className="form-control" 
                                onChange={(e)=>{                                 
                                    try {
                                        setRelease(e.target.value);
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
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["release"]}</> : ""}
                                </h5>
                    Year: <input type="text" 
                                value={year} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{
                                    try {
                                        setYear(e.target.value);
                                        validator(e.target.value,"year");
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
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["year"]}</> : ""}
                                </h5>
                    Video ID: <input type="text" 
                                value={link} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{
                                    try {
                                        setLink(e.target.value);
                                        validator(e.target.value,"youtubeID");
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
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["youtubeID"]}</> : ""}
                                </h5>
                                <br/>
                                <h5 className="text-danger">
                                    {hasErrors ? <>{errors["main"]}</> : ""}
                                </h5>
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
            view = <Form  />
        }
        else {
            view = <input type="button" value="Add New Song" className="btn btn-primary" onClick={()=>{setShowNew(true)}} />
        }
    }
   return(<div>{view}</div>)

}