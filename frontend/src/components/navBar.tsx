import React from "react";
import "./navBar.css";
import { Dropdown } from 'react-dropdown-now';
import 'react-dropdown-now/style.css';
const server = process.env.REACT_APP_SERVER ? process.env.REACT_APP_SERVER :"http://localhost:4000/graphql";

type dropdown_type = {
  value:string,
  label:string,
  color:string
}
type props_type= {
  Page?:number,
  filter:any,
  search:any
}
type options_type = {
  //{value:item.value, view:view, label:view}
  value?:string,
  view?:JSX.Element,
  label?:JSX.Element | string
}


/**
 * 
 * @description builds menu search and dropdown elements.
 * @param {filter} props 
 * @returns {React.NavBar} NavBar
 */

export function NavBar(props:props_type): JSX.Element {
  let pageDisplay:null = null;
  
  return (
    <div className="navBar">
      <div className="firstColumn">{pageDisplay}</div>
      <div className="secondColumn">
        <div className="search">{<FSearch filter={props.filter} search={props.search} />}</div>{" "}
      </div>
    </div>
  );
}
function FSearch(props:props_type) {
  const [dropdown,setDropdown]= React.useState<dropdown_type[]>([]);
  const [search,setSearch] = props.search;
  const [filter,setFilter] = props.filter;
  React.useEffect(()=>{
  console.log(server);
  setDropdown([{
    value:'release',
    label:'Release',
    color:'red'
  },
  {
    value:"AI",
    label:"AI",
    color:"blue"
  },
  {
    value:'artist_name',
    label:'Artist name',
    color:'green'
  },
  {
    value:'year',
    label:'Year',
    color:'brown'
  }
  ])
  },[]);
  let options:options_type[] = [];
  if(dropdown){
   options = dropdown.map((item,index)=>{
    let colors = item.color
    let style:React.CSSProperties = {
      color: `${colors}`,
    };
    let view = <h6 style={style}>{item.label}</h6>
    return {value:item.value, view:view, label:view}
  });
  let startOption:{value:string,label:string}  = {value:'title',label:'Title'}
  options = [startOption,...options];
  }
  let dp = <Dropdown placeholder="Title" className="searchDropdown" options={options} onChange={(value) => {setFilter(value.value); setSearch("")}}/>
  let input = <input type='text' placeholder="Search" value={search}  className='searchInput rdn-control' onChange={(e)=>{
    setSearch(e.target.value);
    e.preventDefault();
  }} />
  return <>{input}{dp}</>;
}
