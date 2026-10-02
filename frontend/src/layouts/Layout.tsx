import './Layout.css'
import SideBar from "../components/SideBar/SideBar";
import BottomNav from '../components/BottomNav/BottomNav';
import { Outlet, useLocation } from "react-router-dom";
import { AnimatePresence } from 'framer-motion';
import VerticalTransition from '../components/Animations/VerticalTransition';

function Layout() {

    const location = useLocation();

    return (
        <div className="layout-container">

            <SideBar />

            <main className="main-content">

                <AnimatePresence mode="wait">
                    <VerticalTransition key={location.pathname}>
                        <Outlet />
                    </VerticalTransition>
                </AnimatePresence>

            </main>

            <BottomNav name='Jonh Doe' photoUrl='https://picsum.photos/200/300'/>

        </div>
    );
}


export default Layout;