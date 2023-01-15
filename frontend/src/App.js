import React from "react";
import { NavBar } from "./components/navBar";
import { Login } from "./login";
import { query } from "./functions/queries";
import { Card } from "./components/cards";
import "./App.css";
import YTSearch from "youtube-api-search";
const YOUTUBE_KEY  = process.env.REACT_APP_API_KEY_YT;

const UserContext = React.createContext(null);



function App() {
  const [search, setSearch] = React.useState("");
  const [filter, setFilter] = React.useState("title");
  const [page, setPage] = React.useState(0);
  const [user, setUser] = React.useState();
  const [data, setData] = React.useState([]);
  const [userData, setUserData] = React.useState([]);
  const [predictions, setPredictions] = React.useState([]);
  const [excludememo,setExcludememo] = React.useState([]);

  const [video,setVideo] = React.useState(null);
  const videoSearch = (term) => {
    console.log("click");
    YTSearch({key:YOUTUBE_KEY, term:term},(videos) =>{
      setVideo(videos[0]);
    })
  }
 const getAllData = React.useCallback(async (user,excludes=[])=>{
    const q = `
    query Songs($filters:songFilters!) {
      listSongs(filters:$filters){
        errors,
        success,
        songs{
          id,
          song_id,
          title,
          release,
          artist_name,
          year
        }
      }
    }
    `; 
     query(q, { filters: { search: search, filter: filter } }, user, (d) => {
      if (d.listSongs.success) {
        let data = d.listSongs.songs;
        if(excludes){
          data = data.filter((v)=>{
            return  !excludes.includes(v.song_id);
          });
        }
        setData(data);
      }
    });
  });
  const getRatedData = async (user,excludes=[])=>{
    const q = `
    query Songs($filters:songFilters!) {
      listSongs(filters:$filters){
        errors,
        success,
        songs{
          id,
          song_id,
          title,
          release,
          artist_name,
          year,
          play_count
        }
      }
    }
    `;
    let ids = [];
   await query(q,{ filters: 
      { search: search, 
        filter: filter, 
        user: user.id } },
      user,
      (d) => {
        if (d.listSongs.success && d.listSongs.songs.length > 0) {
          let data = [];
          d.listSongs.songs.forEach((v,i)=>{
            if(excludes) {
              if(!excludes.includes(v.id)) {
                data.push(v);
                ids.push(v.song_id);
              }
            }
            else {
              data.push(v);
              ids.push(v.song_id);
            }
          });  
          setUserData(data);
        }
      });
      return ids;
  }

  const getPredictedData = async (user,excludes=[])=>{
    const q = `
    query predictSong($songInput:songInput!){
      predictSong(query:$songInput){
        success,
        errors,
        predict{
          id,
          score
        }
      }
    }
    `;
    const ids = [];
    await query(q,{songInput: {user_id: parseInt(user.id)}},user,
              (d) => {
                const allData = [];
                console.log(d.predictSong);
                if(d.predictSong.success){
                d.predictSong.predict.forEach(async (v,i)=>{
                  const q = `
                  query findSong($id:ID!){
                    getSong(id:$id){
                      success,
                      errors,
                      song{
                        id,
                        song_id,
                        title,
                        release,
                        artist_name,
                        year
                      }
                    }
                  }
                  `;
                await query(q,{"id":v.id},user,(data)=>{
                  console.log(data);
                    if(data.getSong.success){
                      allData.push(data.getSong.song);
                      ids.push(v.song_id);
                    }
                  });

                });
                console.log(allData);
                setPredictions(allData);
              }
              }
    );
    return ids;
  };
  async function load(){
    console.log("load run!")
    if (user) {
      let allexcludes = [];
     await getRatedData(user)
      .then((excludes)=>{
        if(excludes) {
          console.log(excludes);
          allexcludes = [...excludes,...allexcludes];
          console.log(allexcludes);
          getPredictedData(user,allexcludes)
          .then((excludes)=>{
            console.log(excludes);
            if(excludes) {
              allexcludes = [...excludes,...allexcludes];
              console.log(allexcludes)
              getAllData(user,allexcludes);
            }
            else {
              getAllData(user,allexcludes);
            }
          })
        }
        else{
          getAllData(user);
        }
      })
      setExcludememo(allexcludes);
    
    }
  }
  React.useEffect(() => {
    if(search.length > 0 && user){
      getAllData(user,excludememo);
    }
    else{
      load()
    }
  }, [user,search]);


  function View(props) {
    let data = props.data.map((val, index) => {
      return (
        <Card
          key={"card_" + index}
          title={val.title}
          header={val.artist_name}
          text={val.release + " " + val.year}
          song={val}
          style=""
          excludememo={excludememo}
          setExcludememo={setExcludememo}
          videoSearch = {videoSearch}
          refresh = {load}
        />
      );
    });
    let userD = "";
    if (props.userData) {
      userD = props.userData.map((val, index) => {
        return (
          <Card
            key={"user_card_" + index}
            title={val.title}
            header={val.artist_name}
            text={val.release + " " + val.year}
            song={val}
            videoSearch = {videoSearch}
            style = {'scored'}
          />
        );
      });
    }
    let recommended = "";
    if(props.recommendedData) {
      console.log(props.recommendedData);
      recommended = props.recommendedData.map((val,index)=>{
       return (<Card
        key={"recommended_key_" + index}
        title={val.title}
        header={val.artist_name}
        text={val.release + " " + val.year}
        song={val}
        style={'predicted'}
        excludememo={excludememo}
        setExcludememo={setExcludememo}
        videoSearch = {videoSearch}
        refresh = {load}
      />);
      });
    }

    return (
      <div className="mid_container">
        {video?video:""}
        {recommended}
        {userD}
        {data}
      </div>
    );
  }
  return (
    <UserContext.Provider value={[user, setUser]}>
      <div className="App">
        <Login />
        {user && (
          <NavBar
            filter={[filter, setFilter]}
            search={[search, setSearch]}
            Page={page}
          />
        )}
        {user && data && <View data={data} userData={userData} recommendedData={predictions} />}
      </div>
    </UserContext.Provider>
  );
}
export { App, UserContext };
