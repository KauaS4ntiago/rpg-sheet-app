import './BottomNav.css'
import { NavLink } from 'react-router-dom'
import { Map, ScrollText, Users } from 'lucide-react';

interface BottomNavProps {
    name: string,
    photoUrl: string
}

function BottomNav({ name, photoUrl }: BottomNavProps) {
    return (
        <div className='bottomNav-container'>
            <ul className="bottomNav-links">
                <NavLink
                    to="/characters"
                >
                    <Users size={35}/>
                    Characters
                </NavLink>

                <NavLink
                    to="/campaigns"
                >
                    <Map size={35}/>
                    Campaigns
                </NavLink>

                <NavLink
                    to="/master"
                >
                    <ScrollText size={35}/>
                    Master
                </NavLink>

                <NavLink to="/profile">
                    <img
                        className="profile-pic"
                        alt={name}
                        src={photoUrl}
                    />
                    <span>Profile</span>
                </NavLink>
            </ul>
        </div>
    )
}


export default BottomNav;