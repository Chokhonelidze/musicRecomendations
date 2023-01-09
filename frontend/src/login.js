import React from "react";
import { UserContext } from "./App";
import { validator } from "./functions/validator";
import { query } from "./functions/queries";
export function Login() {
    const [user,setUser] = React.useContext(UserContext);
    const [email,setEmail] = React.useState("");
    const [password,setPassword] = React.useState("");
    function login() {
        if(email && validator(email,'email')) {
            const obj = {
                email:email,
                password:password
            }
            const q= `
            query login($query: loginInput!) {
                login(query: $query) {
                    error,
                    success,
                    user{
                        id,
                        email,
                        role,
                    }
                }
            }
            `;
            query(q,{query:obj},user,(obj)=>{
                if(obj.login.user)
                setUser(obj.login.user)
            });

        }
    }
    return(
        <>
        {user?<div onClick={()=>{setUser(null)}}>logout</div>:
        <div>
            <input type="text" value={email} onChange={(e)=>{setEmail(e.target.value)}} />
            <input type="password" value={password} onChange={(e)=>{setPassword(e.target.value)}} />
            <button type="submit" onClick={login} >login</button>
        </div>
        }
        </>
    )
}