/** @jsxRuntime classic */
/** @jsx React.createElement */
/// <reference types="react" />
import React from "react";
import { NavBar } from "./components/navBar";
import { Login } from "./login";
import { query } from "./functions/queries";
import { Card } from "./components/cards";
import { CreateSong } from "./createSong";
import "./App.css";
import YTSearch from "youtube-api-search-typed/dist";
import ReactPlayer from "react-player";
import {
  user_type,
  pureSong_type,
  pureSongsResult_type,
  song_type,
  predictOutput_type,
  songsResult_type,
  getSong_type,
  prediction_type,
} from "./functions/types";
const YOUTUBE_KEY = process.env.REACT_APP_API_KEY_YT;

const UserContext = React.createContext({});

function App(): React.JSX.Element {
  const [search, setSearch] = React.useState("");
  const [filter, setFilter] = React.useState("title");
  const [offset, setOffset] = React.useState(0);
  const limit = 10;
  const [user, setUser] = React.useState<user_type>();
  const [data, setData] = React.useState<pureSong_type[]>([]);
  const [userData, setUserData] = React.useState<song_type[]>([]);
  const [predictions, setPredictions] = React.useState<pureSong_type[]>([]);
  const [excludememo, setExcludememo] = React.useState<number[]>([]);
  const [loading, setLoading] = React.useState<boolean>(false);
  const [playerUrl, setPlayerUrl] = React.useState<string>("");

  const [video, setVideo] = React.useState<string>("");

  React.useEffect(() => {
    if (video && user) {
      setLoading(true);
      fetch(video)
        .then((response) => response.blob())
        .then((blob) => {
          // 2. Create a local object URL that ReactPlayer can stream
          const localUrl = URL.createObjectURL(blob);
          setPlayerUrl(localUrl);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error loading audio stream:", error);
          setLoading(false);
        });
    }
    return () => {
      if (playerUrl) {
        URL.revokeObjectURL(playerUrl);
      }
    };
  }, [video]);

  const videoSearch = async (
    term: string,
    id: number,
    link: string = "",
    localLink: string = "",
  ) => {
    if (localLink) {
      let newLocalLink = process.env.REACT_APP_DOWNLOADSERVER + localLink;
      setVideo(newLocalLink);
      return newLocalLink
    } else {
      try {
        await YTSearch({ key: YOUTUBE_KEY as string, term: term }, async (videos: any) => {
          console.log(videos);
          const q = `
        mutation UpdateAllSongs($song:updateAllSongLinksInput){
          updateAllSongLinks(song:$song){
            success,
            errors,
            ids,
            local_link
          }
        }
        `;
          type response = {
            updateAllSongLinks?: {
              success: boolean;
              errors: string[];
              ids: number[];
              local_link: string;
            };
          };
          if (videos && videos[0]) {
            let newlink = `//www.youtube.com/embed/${videos[0].id.videoId as string}?autoplay=1&mute=0`;
            newlink = `https://www.youtube.com/watch?v=${videos[0].id.videoId as string}?autoplay=1&mute=0`;
            console.log(newlink);
            await query(
              q,
              {
                song: { id: parseInt(String(id) as string), local_link: newlink },
              },
              user as user_type,
              (d: response) => {
                console.log(videos[0] as Object);
                console.log(d);
                if (d?.updateAllSongLinks?.success) {
                  let newLocalLink = process.env.REACT_APP_DOWNLOADSERVER + d.updateAllSongLinks.local_link;
                  setVideo(newLocalLink);
                  return newLocalLink
                }
              },
            );
          }
        });
      } catch (error) {
        console.error("Error searching YouTube:", error);
      }
    }
  };
  const getAllData = async (user: user_type, excludes: number[] = []) => {
    console.log("all data is running");
    const q = `
    query pureSongs($filters:pureSongFilters!){
      listPureSongs(filters:$filters){
        success,
        errors,
        data{
          song_id,
          title,
          artist_name,
          release,
          year,
          video_link,
          local_link
        }
      }
    }
    `;
    query(
      q,
      {
        filters: {
          search: search,
          filter: filter,
          offset: offset,
          limit: limit,
        },
      },
      user,
      (d: pureSongsResult_type) => {
        if (d.listPureSongs.success) {
          let data_temp: pureSong_type[] = d.listPureSongs.data;
          console.log(excludes);
          console.log(data_temp);
          let result: pureSong_type[] | [] = [];
          if (excludes) {
            result = data_temp.filter(
              (v: pureSong_type): pureSong_type | any => {
                return !excludes.includes(v.song_id as number);
              },
            );
          }
          setData(result);
        }
      },
    );
  };

  const getRatedData = async (user: user_type, excludes: number[] = []) => {
    console.log("rated data is runing");
    const q = `
    query Songs($filters:songFilters!) {
      listSongs(filters:$filters){
        errors,
        success,
        data{
          id,
          song_id,
          title,
          release,
          artist_name,
          year,
          local_link,
          play_count
        }
      }
    }
    `;
    let ids: any[] = [];
    await query(
      q,
      { filters: { search: search, filter: filter, user: user.id } },
      user,
      (d: songsResult_type) => {
        if (d.listSongs.success && d.listSongs.data.length > 0) {
          let data: song_type[] = [];
          d.listSongs.data.forEach((v, i: number) => {
            if (excludes) {
              if (!excludes.includes(v.id as number)) {
                data.push(v);
                ids.push(v.song_id);
              }
            } else {
              data.push(v);
              ids.push(v.song_id);
            }
          });
          setUserData(data);
        }
      },
    );
    return ids;
  };

  const getPredictedData = async (user: user_type, excludes: number[] = []) => {
    const q = `
    query predictSong($songInput:songInput!){
      predictSong(query:$songInput){
        success,
        errors,
        data{
          id,
          score,
          common
        }
      }
    }
    `;
    const ids: number[] = [];
    await query(
      q,
      { songInput: { user_id: user.id } },
      user,
      (d: predictOutput_type) => {
        const allData: pureSong_type[] = [];
        console.log(d.predictSong);
        if (d.predictSong.success) {
          d.predictSong?.data?.forEach(
            async (v: prediction_type, i: number) => {
              const q = `
                  query findSong($id:ID!){
                    getSong(id:$id){
                      success,
                      errors,
                      data{
                        id,
                        song_id,
                        title,
                        release,
                        artist_name,
                        local_link,
                        year
                      }
                    }
                  }
                  `;
              await query(q, { id: v.id }, user, (data: getSong_type) => {
                console.log(data);
                if (data.getSong.success) {
                  let song = data.getSong.data;
                  song["predict"] = v.score;
                  song["common"] = v.common;
                  allData.push(song);
                  ids.push(v.id as number);
                }
              });
            },
          );
          setPredictions(allData);
        }
      },
    );
    return ids;
  };
  async function load() {
    console.log("load run!");
    if (user) {
      let allexcludes: number[] = [];
      await getRatedData(user as user_type).then((excludes) => {
        if (excludes) {
          console.log(excludes);
          allexcludes = [...excludes, ...allexcludes];
          console.log(allexcludes);
          getPredictedData(user as user_type, allexcludes).then((excludes) => {
            console.log(excludes);
            if (excludes) {
              allexcludes = [...excludes, ...allexcludes];
              console.log(allexcludes);
              getAllData(user as user_type, allexcludes);
            } else {
              getAllData(user as user_type, allexcludes);
            }
          });
        } else {
          getAllData(user as user_type);
        }
      });
      setExcludememo(allexcludes);
    }
  }
  React.useEffect(() => {
    if (search.length > 0 && user) {
      setOffset(0);
      const timer = setTimeout(() => {
        setUserData([]);
        getRatedData(user as user_type);
        getAllData(user as user_type, excludememo);
        console.log("refresh started");
      }, 2000);
      return () => clearTimeout(timer);
    } else {
      load();
    }
  }, [user, search]);

  function View(props: any) {
    const loadMore = async () => {
      /**
       *  this is the callback function used for data load.
       */
      if (filter === "AI") {
        return false;
      }
      const [data, setData] = props.dataSet;
      const q = `
      query pureSongs($filters:pureSongFilters!){
        listPureSongs(filters:$filters){
          success,
          errors,
          data{
            song_id,
            title,
            artist_name,
            release,
            year,
            video_link,
            local_link
          }
        }
      }
      `;
      if (
        document.scrollingElement &&
        window.innerHeight + document.documentElement.scrollTop + 1 >=
          document.scrollingElement.scrollHeight
      ) {
        let newOffset = offset + 10;
        let newLimit = limit;
        console.log(newLimit, newOffset);

        function mergeData(newData: any) {
          setOffset(newOffset);
          if (
            newData.listPureSongs.data &&
            newData.listPureSongs.data.length > 0
          ) {
            const existingIds = new Set(data.map(val => val.song_id));
            const newSongs = newData.listPureSongs.data.filter((val: any) => 
              !existingIds.has(val.song_id)
            );
            let allData = [...data, ...newSongs];
            console.log(allData);
            allData = allData.filter((val) => {
              return !excludememo.includes(parseInt(val.song_id));
            });
            setData(allData);
          }
        }
        let parameters = {
          search: search,
          filter: filter,
          offset: newOffset,
          limit: newLimit,
        };

        await query(q, { filters: parameters }, user as user_type, mergeData);
      }
    };
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
          videoSearch={videoSearch}
          refresh={load}
        />
      );
    });
    let userD = "";
    if (props.userData) {
      userD = props.userData.map((val: any, index: number) => {
        return (
          <Card
            key={"user_card_" + index}
            title={val.title}
            header={val.artist_name}
            text={val.release + " " + val.year}
            song={val}
            videoSearch={videoSearch}
            style={"scored"}
          />
        );
      });
    }
    let recommended = "";
    if (props.recommendedData) {
      console.log(props.recommendedData);
      recommended = props.recommendedData.map((val: any, index: number) => {
        return (
          <Card
            key={"recommended_key_" + index}
            title={val.title}
            header={val.artist_name}
            text={val.release + " " + val.year}
            song={val}
            style={val.common ? "special" : "predicted"}
            excludememo={excludememo}
            setExcludememo={setExcludememo}
            videoSearch={videoSearch}
            refresh={() => {
              setData([]);
              setPredictions([]);
              setUserData([]);
              load();
            }}
            predict={val.predict}
          />
        );
      });
    }
    React.useEffect(() => {
      window.addEventListener("scroll", loadMore);
      return () => {
        window.removeEventListener("scroll", loadMore);
      };
    }, [loadMore]);
    return (
      <div className="mid_container">
        {search ? "" : recommended}
        {userD}
        {alldata}
      </div>
    );
  }
  const ViewMemo = React.useMemo(() => {
    return (
      <View
        dataSet={[data, setData]}
        userData={userData}
        recommendedData={predictions}
      />
    );
  }, [data, userData, predictions]);
  return (
    <UserContext.Provider value={[user, setUser]}>
      <div className="App">
        <Login />
        <CreateSong />
        {user != null && (
          <NavBar
            filter={[filter, setFilter]}
            search={[search, setSearch]}
            Page={offset}
          />
        )}
        <div className="center">
          {loading ? (
            <div className="loading">Loading...</div>
          ) : playerUrl && user ? (
            <>
            <audio src={playerUrl} controls autoPlay style={{ width: '220px' }} />
         
            {/* <ReactPlayer
              url={playerUrl}
              playing={true}
              width={220}
              height={220}
              controls={true}
              config={{ file: { forceAudio: true } }}
            />
             */}
            </>
          ) : (
            ""
          )}
        </div>
        {user && data && ViewMemo}
      </div>
    </UserContext.Provider>
  );
}
export { App, UserContext };
