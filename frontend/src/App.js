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
  const [offset, setOffset] = React.useState(0);
  const limit = 10;
  const [user, setUser] = React.useState();
  const [data, setData] = React.useState([]);
  const [userData, setUserData] = React.useState([]);
  const [predictions, setPredictions] = React.useState([]);
  const [excludememo,setExcludememo] = React.useState([]);

  const [video,setVideo] = React.useState(null);
  const videoSearch = (term,id,link=null) => {
    console.log("click");
    if(link) {
      setVideo(link);
    }
    else{
      YTSearch({key:YOUTUBE_KEY, term:term},(videos) =>{
        
      const q = `
      mutation UpdateAllSongs($song:updateAllSongLinksInput){
        updateAllSongLinks(song:$song){
          success,
          errors,
          ids
        }
      }
      `;
        let newlink = `//www.youtube.com/embed/${videos[0].id.videoId}?autoplay=1&mute=0`;
        query(q,{"song":{id:id,link:newlink}},user,(d)=>{ 
          console.log(videos[0]);
          console.log(d);
        })
        setVideo(newlink);
      })
    }
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
          link,
          year
        }
      }
    }
    `; 
     query(q, { filters: { search: search, filter: filter, offset:offset,limit:limit } }, user, (d) => {
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
          link,
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
                        link,
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
      setOffset(0);
    }
    else{
      load()
    }
  }, [user,search]);

  
  function View(props) {
    const loadMore = React.useCallback(() => {
      /**
       *  this is the callback function used for data load.
       */
      const [data,setData] = props.dataSet;
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
            link,
            year
          }
        }
      }
      `; 
      if (
        window.innerHeight + document.documentElement.scrollTop+1 >=
        document.scrollingElement.scrollHeight
      ) {
        let newOffset = offset+10;
        let newLimit = limit;
       console.log(newLimit,newOffset);
       
      function mergeData(newData) {
        setOffset(newOffset);
        if(newData.listSongs.songs && newData.listSongs.songs.length > 0) {
          setData([...data,...newData.listSongs.songs]);
        }
      }
      let parameters = {
        search: search, 
        filter: filter, 
        offset:newOffset,
        limit:newLimit
      }
  
        query(q,{filters:parameters},user,mergeData);
      }
     
    }, [data, setData, limit,filter,offset,search]);
    let alldata = data.map((val, index) => {
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
    React.useEffect(()=>{
      window.addEventListener("scroll", loadMore);
      return () => {
        window.removeEventListener("scroll", loadMore);
      };
    },[loadMore])
    return (
      <div className="mid_container">
        {recommended}
        {userD}
        {alldata}
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
            Page={offset}
          />
        )}
        {video && user?<iframe src={video} name="youtube embed" allow="autoplay; encrypted-media" autoPlay="1"> </iframe>:""}
        {user && data && <View dataSet={[data,setData]} userData={userData} recommendedData={predictions} />}
      </div>
    </UserContext.Provider>
  );
}
export { App, UserContext };
