import SideBar from "../components/SideBar/SideBar";
import { Outlet } from "react-router-dom";

function Layout() {
  return (
    <div className="layout-container">
        <SideBar/>
        <main className="main-content">
            <Outlet/>
        </main>
    </div>
  )
}


export default Layout;