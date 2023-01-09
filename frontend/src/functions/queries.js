const server = process.env.REACT_APP_SERVER ? process.env.REACT_APP_SERVER :"http://localhost:3000";

/**
 * @description function is used to get pockemons from database.
 * @param {String} q 
 * @param {Array} values 
 * @param {Function} callback 
 * @returns {Array} pokemons
 */
export async function query(q,values,user,callback) {
    let headers =  {
      "Content-Type": "application/json",
      Accept: "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers":
      "Origin, X-Requested-With, Content-Type, Accept"
    };
    if(user) {
      //headers["authorization"] = `${user.user.name} ${user.accessToken}`;
    }
    await fetch(server, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
          query: q,
          variables: values,
        }),
      })
        .then((res) => res.json())
        .then((info, err) => {
             if(!err) {
               callback(info.data);
             }
             else {
                 console.log(err);
             }
        });
}
