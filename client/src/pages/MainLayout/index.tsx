import Footer from "@/pages/MainLayout/Footer";
import MainNav from "./MainNav";
import { Outlet } from "react-router-dom";
import AIAssistantWindow from '@/components/AIAssistant/AIAssistantWindow';

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainNav />
      <main className="flex-1">
        <Outlet />
      </main>
      <AIAssistantWindow />
      <Footer />
    </div>
  );
}
