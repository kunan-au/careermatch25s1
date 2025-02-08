import Footer from "@/pages/MainLayout/Footer";
import MainNav from "./MainNav";
import { Outlet } from "react-router-dom";

export default function MainLayout() {
  return (
    <>
      <MainNav />
      <Outlet />
      <Footer />
    </>
  );
}
