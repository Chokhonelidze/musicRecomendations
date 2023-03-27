import React from "react";
import { NavBar } from "./components/navBar";
import { Login } from "./login";
import { query } from "./functions/queries";
import { Card } from "./components/cards";
import { CreateSong } from "./createSong";
import "./App.css";
import YTSearch from "youtube-api-search-typed/dist";
import ReactPlayer from "react-player";
import { user_type,pureSong_type,pureSongsResult_type, song_type, predictOutput_type, songsResult_type, getSong_type, prediction_type } from "./functions/types";
const YOUTUBE_KEY  = process.env.REACT_APP_API_KEY_YT;

const UserContext = React.createContext({});



function App() {
  const [search, setSearch] = React.useState("");
  const [filter, setFilter] = React.useState("title");
  const [offset, setOffset] = React.useState(0);
  const limit = 10;
  const [user, setUser] = React.useState<user_type|{}>({});
  const [data, setData] = React.useState<pureSong_type[]>([]);
  const [userData, setUserData] = React.useState<song_type[]>([]);
  const [predictions, setPredictions] = React.useState<pureSong_type[]>([]);
  const [excludememo,setExcludememo] = React.useState<number[]>([]);

  const [video,setVideo] = React.useState<string>("");
  const videoSearch = (term:string,id:number,link:string ="") => {
    console.log("click");
    if(link) {
      setVideo(link);
    }
    else{
      YTSearch({key:YOUTUBE_KEY as string, term:term},(videos) =>{
        
      const q = `
      mutation UpdateAllSongs($song:updateAllSongLinksInput){
        updateAllSongLinks(song:$song){
          success,
          errors,
          ids
        }
      }
      `;
      type response = {
        sucess:boolean,
        errors:[string];
        ids:[number] 
      }
      if(videos && videos[0]) {
        let newlink = `//www.youtube.com/embed/${videos[0].id.videoId as string}?autoplay=1&mute=0`;
        query(q,{"song":{id:parseInt(String(id) as string),link:newlink}},user as user_type,(d:response)=>{ 
          console.log(videos[0] as Object);
          console.log(d);
        })
        setVideo(newlink);
      }})
      
    }
  }
 const getAllData = async (user:user_type,excludes:number[]=[])=>{
  console.log("all data is running")
    const q = `
    query pureSongs($filters:pureSongFilters!){
      listPureSongs(filters:$filters){
        success,
        errors,
        songs{
          song_id,
          title,
          artist_name,
          release,
          year,
          link,
        }
      }
    }
    `; 
     query(q, { filters: { search: search, filter: filter, offset:offset,limit:limit } }, user, (d:pureSongsResult_type) => {
      if (d.listPureSongs.success) {
        let data_temp:pureSong_type[]  = d.listPureSongs.songs;
        console.log(excludes);
        console.log(data_temp);
        let result:pureSong_type[] | [] = []
        if(excludes){
            result = data_temp.filter((v:pureSong_type):pureSong_type | any =>{
            return  !excludes.includes(v.song_id as number);
            
          });
        }
        setData(result);
      }
    });
  }

  const getRatedData = async (user:user_type,excludes:number[]=[])=>{
    console.log("rated data is runing")
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
    let ids: any[] = [];
   await query(q,{ filters: 
      { search: search, 
        filter: filter, 
        user: user.id } },
      user,
      (d:songsResult_type) => {
        if (d.listSongs.success && d.listSongs.songs.length > 0) {
          let data:song_type[] = [];
          d.listSongs.songs.forEach((v,i:number)=>{
            if(excludes) {
              if(!excludes.includes(v.id as number)) {
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

  const getPredictedData = async (user:user_type,excludes:number[]=[])=>{
    const q = `
    query predictSong($songInput:songInput!){
      predictSong(query:$songInput){
        success,
        errors,
        predict{
          id,
          score,
          common
        }
      }
    }
    `;
    const ids:number[] = [];
    await query(q,{songInput: {user_id: user.id}},user,
              (d:predictOutput_type) => {
                const allData:pureSong_type[] = [];
                console.log(d.predictSong);
                if(d.predictSong.success){
                d.predictSong.predict.forEach(async (v:prediction_type,i:number)=>{
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
                await query(q,{"id":v.id},user,(data:getSong_type)=>{
                  console.log(data);
                    if(data.getSong.success){
                      let song = data.getSong.song
                      song['predict'] = v.score;
                      song['common'] = v.common;
                      allData.push(song);
                      ids.push(v.id as number);
                    }
                  });

                });
                setPredictions(allData);
              }
              }
    );
    return ids;
  };
  async function load(){
    console.log("load run!")
    if (user) {
      let allexcludes:number[] = [];
     await getRatedData(user as user_type)
      .then((excludes)=>{
        if(excludes) {
          console.log(excludes);
          allexcludes = [...excludes,...allexcludes];
          console.log(allexcludes);
          getPredictedData(user as user_type,allexcludes)
          .then((excludes)=>{
            console.log(excludes);
            if(excludes) {
              allexcludes = [...excludes,...allexcludes];
              console.log(allexcludes)
              getAllData(user as user_type,allexcludes);
            }
            else {
              getAllData(user as user_type,allexcludes);
            }
          })
        }
        else{
          getAllData(user as user_type);
        }
      })
      setExcludememo(allexcludes);
    
    }
  }
  React.useEffect(() => {
    if(search.length > 0 && user){
      setOffset(0);
      const timer = setTimeout(() => {
        setUserData([]);
        getRatedData(user as user_type);
        getAllData(user as user_type,excludememo);
        console.log("refresh started");
      }, 2000)
      return () => clearTimeout(timer)
    }
    else{
      load()
    }
  }, [user,search]);

  
  function View(props:any) {
    const loadMore = () => {
      /**
       *  this is the callback function used for data load.
       */

      const [data,setData] = props.dataSet;
      const q = `
      query pureSongs($filters:pureSongFilters!){
        listPureSongs(filters:$filters){
          success,
          errors,
          songs{
            song_id,
            title,
            artist_name,
            release,
            year,
            link,
          }
        }
      }
      `; 
      if (
        document.scrollingElement &&
        window.innerHeight + document.documentElement.scrollTop+1 >=
        document.scrollingElement.scrollHeight
      ) {
        let newOffset = offset+10;
        let newLimit = limit;
       console.log(newLimit,newOffset);
       
      function mergeData(newData:any) {
        setOffset(newOffset);
        
        if(newData.listPureSongs.songs && newData.listPureSongs.songs.length > 0) {
          let allData = [...data,...newData.listPureSongs.songs];
          console.log(allData);
          allData = allData.filter((val)=>{
            return !excludememo.includes(parseInt(val.song_id));
          })
          setData(allData);
        }
      }
      let parameters = {
        search: search, 
        filter: filter, 
        offset:newOffset,
        limit:newLimit
      }
  
        query(q,{filters:parameters},user as user_type,mergeData);
      }
     
    }
    let alldata = data.map((val, index) => {
      return (
        <Card
          key={"card_" + index}
          title={val.title}
          header={val.artist_name}
          text={val.release + " " + val.year}
          song={val}
          style=" "
          excludememo={excludememo}
          setExcludememo={setExcludememo}
          videoSearch = {videoSearch}
          refresh = {load}
        />
      );
    });
    let userD = "";
    if (props.userData) {
      userD = props.userData.map((val:any, index:number) => {
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
      recommended = props.recommendedData.map((val:any,index:number)=>{
       return (<Card
        key={"recommended_key_" + index}
        title={val.title}
        header={val.artist_name}
        text={val.release + " " + val.year}
        song={val}
        style={val.common?"special":"predicted"}
        excludememo={excludememo}
        setExcludememo={setExcludememo}
        videoSearch = {videoSearch}
        refresh = {()=>{
          setData([]);
          setPredictions([]);
          setUserData([]);
          load()
        }}
        predict = {val.predict}
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
        {search?"":recommended}
        {userD}
        {alldata}
      </div>
    );
  }
  const ViewMemo = React.useMemo(()=>{
  return <View dataSet={[data,setData]} 
                userData={userData} 
                recommendedData={predictions} />}
                ,[data,userData,predictions]);
  return (
    <UserContext.Provider value={[user, setUser]}>
      <div className="App">
        
        <Login />
        <CreateSong />
        {user && (
          <NavBar
            filter={[filter, setFilter]}
            search={[search, setSearch]}
            Page={offset}
          />
        )}
        <div className="center">
        {video && user?<ReactPlayer
        url={video}
        playing={true}
        width={220}
        height={220}
        />:""}
        </div>
        {user && data && ViewMemo}
      </div>
    </UserContext.Provider>
  );
}
export { App, UserContext };
