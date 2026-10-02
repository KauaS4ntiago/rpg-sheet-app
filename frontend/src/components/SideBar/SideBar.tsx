import './SideBar.css';

import { NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';

import Profile from '../Profile/Profile';

import { LogOut, Menu, X } from 'lucide-react';

import { Map, ScrollText, Users } from 'lucide-react';

function SideBar() {

    const Navigate = useNavigate();

    const [isMenuOpen, setIsMenuOpen] = useState(false);

    function handleNavigate() {
        setIsMenuOpen(false);
    }

    return (
        <div className="sidebar-container">

            {/* HEADER / PROFILE */}
            <div className="sidebar-header">

                <Profile
                    username="John Doe"
                    email="john.doe@example.com"
                    photoUrl="https://picsum.photos/200/300"
                />

                {/* HAMBURGER */}
                <button
                    className="menu-button"
                    onClick={() => setIsMenuOpen(prev => !prev)}
                    aria-label="Abrir menu"
                >
                    {isMenuOpen
                        ? <X size={30} />
                        : <Menu size={30} />
                    }
                </button>

            </div>

            {/* MENU */}
            <div
                className={`sidebar-links-wrapper ${
                    isMenuOpen ? 'menu-open' : ''
                }`}
            >

                <ul className="sidebar-links">

                    <NavLink
                        to="/characters"
                        onClick={handleNavigate}
                    >
                        <Users/>
                        Characters
                    </NavLink>

                    <NavLink
                        to="/campaigns"
                        onClick={handleNavigate}
                    >
                        <Map/>
                        Campaigns
                    </NavLink>

                    <NavLink
                        to="/master"
                        onClick={handleNavigate}
                    >
                        <ScrollText/>
                        Master
                    </NavLink>

                </ul>

                <button
                    className="logout-button"
                    onClick={() => Navigate('/login')}
                >
                    <LogOut size={25} strokeWidth={2.5} />
                    <span>Exit</span>
                </button>

            </div>

        </div>
    );
}

export default SideBar;