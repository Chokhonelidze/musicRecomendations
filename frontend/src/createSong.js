import React from "react";
import { UserContext } from "./App";
import { validator } from "./functions/validator";

export function CreateSong() {
    const [title,setTitle] = React.useState("");
    const [artist_name,setArtist_name] = React.useState("");
    const [link,setLink] = React.useState("");
    const [release,setRelease] = React.useState("");
    const [year,setYear] = React.useState("");
    const [user, setUser] = React.useContext(UserContext);
    const [showNewSong,setShowNew] = React.useEffect(false);

    function Form(props) {
        return (<div className="formConteiner">
            <div className="card mb-3">
                <div className="card-header">
                    Create new Song
                </div>
                <div className="card-body">
                    SongTitle: <input type="text" 
                                value={title} 
                                name="title" 
                                className="form-control" 
                                onChange={(e)=>{
                                    setTitle(e.target.value);
                                    validator(title,"name");
                                }} />
                    Artist Name: <input type="text" 
                                value={artist_name} 
                                name="artist_name" 
                                className="form-control" 
                                onChange={(e)=>{
                                    setArtist_name(e.target.value);
                                    validator(title,"name");
                                }} />
                </div>
            </div>

        </div>);
    }
   return(
    <>
    {(user.role === 1)&&
    showNewSong?"FORM":<input type="button" className="btn btn-primary" onClick={()=>{setShowNew(true)}} />
    }
    </>
   )

}