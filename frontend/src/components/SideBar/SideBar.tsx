import './SideBar.css'
import { NavLink, useNavigate } from "react-router-dom";
import Profile from "../Profile/Profile";
import { LogOut } from 'lucide-react';
import  characters  from '../../assets/characters.svg'
import  company  from '../../assets/company.svg'
import master from '../../assets/master.svg'

function SideBar() {
    const Navigate = useNavigate();
    return (
        <div className="sidebar-container">
            <Profile username="John Doe" email="john.doe@example.com" photoUrl="https://picsum.photos/200/300" />
            <div className='sidebar-links-wrapper'>
                <ul className="sidebar-links">
                    <NavLink to="/characters"><img src={characters}></img>Characters</NavLink>
                    <NavLink to="/company"><img src={company}></img>Company</NavLink>
                    <NavLink to="/master"><img src={master}></img>Master</NavLink>
                </ul>
            </div>
            <button className="logout-button" onClick={() => Navigate('/login')}>
                <LogOut size={25} strokeWidth={2.5}/>
                <span>Exit</span>
            </button>
        </div>
    );
}

export default SideBar;