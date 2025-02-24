import Footer from "@/pages/MainLayout/Footer";
import MainNav from "./MainNav";
import { Outlet } from "react-router-dom";
import { ChatWindow } from '@/components/Chat/ChatWindow';

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainNav />
      <main className="flex-1">
        <Outlet />
      </main>
      <ChatWindow />
      <Footer />
    </div>
  );
}
