import './Layout.css'
import SideBar from "../components/SideBar/SideBar";
import { Outlet } from "react-router-dom";
import { AnimatePresence } from 'framer-motion';
import VerticalTransition from '../components/Animations/VerticalTransition';

function Layout() {
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
    </div>
  )
}


export default Layout;