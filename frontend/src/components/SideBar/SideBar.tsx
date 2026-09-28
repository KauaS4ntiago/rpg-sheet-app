import './SideBar.css'
import { NavLink } from "react-router-dom";
import Profile from "../Profile/Profile";
import { LogOut } from 'lucide-react';

function SideBar() {
    return (
        <div className="sidebar-container">
            <Profile username="John Doe" email="john.doe@example.com" photoUrl="https://picsum.photos/200/300" />
            <ul>
                <NavLink to="/characters">Characters</NavLink>
                <NavLink to="/company">Company</NavLink>
                <NavLink to="/master">Master</NavLink>
            </ul>
            <button className="logout-button">
                <LogOut size={20} />
                <span>Exit</span>
            </button>
        </div>
    );
}

export default SideBar;