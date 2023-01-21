import React from "react";
import { UserContext } from "./App";
import { validator } from "./functions/validator";
import { query } from "./functions/queries";

import "./login.css";
export function Login() {
  const [user, setUser] = React.useContext(UserContext);
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState({});
  const [hasErrors, setHasErrors] = React.useState(false);
  const [createNew, setCreateNew] = React.useState(false);
  const [createUser, setCreateUser] = React.useState("");
  const [createPassword, setCreatePassword] = React.useState("");
  function createNewUser() {
    const q = `
    mutation createUser($user:createUser!){
        createUser(user:$user) {
          success,
          errors,
          user{
            id,
            email,
            role
          }
        }
      }
    `;
    query(q,{"user":{email:createUser,password:createPassword,role:0}},user, (obj)=>{
        if(obj.createUser.user){
          console.log(obj);
            setUser(obj.createUser.user);
            setError({});
            setHasErrors(false);
        }
        else if(obj.createUser.errors) {
            let errors = error;
            errors['mainError'] = obj.createUser.errors.join(",");
            setError(errors);
            setHasErrors(true);
            
        }
    })
  }

  function login() {
    if (email && validator(email, "email")) {
      const obj = {
        email: email,
        password: password,
      };
      const q = `
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
      query(q, { query: obj }, user, (obj) => {
        if (obj.login?.error) {
          let errors = error;
          errors["login"] = obj.login?.error;
          setError(errors);
          setHasErrors(true);
        } else if (error["login"]) {
          setError({});
          setHasErrors(false);
        }
        if (obj.login.user) setUser(obj.login.user);
      });
    }
  }
  return (
    <div className="loginConteiner">
      {user ? (
        <div
          onClick={() => {
            setUser(null);
          }}
        >
          <button className="btn btn-primary" type="button">
            LOGOUT
          </button>
        </div>
      ) : (
        <div className="card mb-3">
          <div className="card-header">
            {createNew ? "OPEN ACCOUNT" : "LOGIN"}
          </div>
          <div className="card-body">
            {createNew ? (
              <>
                <h5>Create User Email:</h5>
                <input
                  className="form-control"
                  type="text"
                  name="user"
                  placeholder="User Email"
                  value={createUser}
                  onChange={(e) => {
                    try {
                      setCreateUser(e.target.value);
                      validator(e.target.value, "email");
                      let errors = error;
                      errors["createEmail"] = "";
                      setError(errors);
                      setHasErrors(false);
                    } catch (err) {
                      let errors = error;
                      errors["createEmail"] = err.email;
                      setError(errors);
                      setHasErrors(true);
                    }
                  }}
                />
                <br />
                <h5 className="text-danger">
                  {hasErrors ? <>{error["createEmail"]}</> : ""}
                </h5>
                <br />
                <input
                  className="form-control"
                  value={createPassword}
                  placeholder="Create Password"
                  type="password"
                  name="password"
                  onChange={(e) => {
                    try {
                        setCreatePassword(e.target.value);
                        validator(e.target.value,"password");
                        let errors = error;
                        errors["createEmail"] = "";
                        setError(errors);
                        setHasErrors(false);
                    }
                    catch(err) {
                        let errors = error;
                        errors["createPassword"] = err.password;
                        setError(errors);
                        setHasErrors(true);
                    }
                  }}
                />
                <br />
                <h5 className="text-danger">
                  {hasErrors ? <>{error["createPassword"]}</> : ""}
                </h5>
                <br />
                <br/>
                <h5 className="text-danger">
                  {hasErrors ? <>{error["mainError"]}</> : ""}
                </h5>
                <br/>
                <input 
                    type="submit"
                    className="btn btn-primary"
                    value = "Create Account"
                    onClick={(e)=>{
                        try{
                            validator(createUser,"email");
                            validator(createPassword,"password");
                            setError({});
                            setHasErrors(false);
                            createNewUser();
                        }
                        catch(err) {
                            let errors = error;
                            if(err.email)errors['createEmail'] = err.email;
                            if(err.password)errors['createPassword'] = err.password;
                            setError(errors);
                            setHasErrors(true);
                        }

                    }} />
                <input 
                    type="button" 
                    value="Login"
                    className="btn btn-primary"
                    onClick={(e)=>{
                        setCreateNew(false);
                    }}
                    />
              </>
            ) : (
              <>
                <h5>User email:</h5>
                <br />
                <input
                  className="form-control"
                  type="text"
                  name="user"
                  placeholder="User email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                  }}
                />
                <br />
                <h5>Password:</h5>
                <br />
                <input
                  className="form-control"
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                  }}
                />
                <br />
                <h5 className="text-danger">
                  {hasErrors ? <>{error["login"]}</> : ""}
                </h5>
                <button
                  className="btn btn-primary"
                  type="submit"
                  onClick={login}
                >
                  LOGIN
                </button>
                <button
                  className="btn btn-primary"
                  type="submit"
                  onClick={() => {
                    setCreateNew(true);
                  }}
                >
                  Open New User
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
