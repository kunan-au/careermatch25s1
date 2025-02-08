import { NavLink } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import { useLogout } from "../SignIn/useLogout";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../SignIn/useUser";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { useProfile } from "../ProfileInfo/useProfile";

const defaultInfoData = {
  email: "string",
  name: "string",
  avatar: "string",
  resume: "string",
};

const MainNav = () => {
  const navigate = useNavigate();
  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "test user" };
  const { status, logout } = useLogout();

  const { user_info } = useProfile(email);

  const { name, avatar } = user_info || defaultInfoData;

  useEffect(() => {
    if (status === "success") {
      setTimeout(() => {
        navigate("/");
      }, 1000);
    }
  }, [status, navigate]);

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="flex justify-between">
      <div className="flex items-center space-x-8 lg:space-x-10 my-4 mx-10">
        <NavLink to="homePage">
          <img className="w-10" src="/company-logo.png" alt="logo" />
        </NavLink>

        <NavLink
          to="jobs"
          className={({ isActive }) =>
            isActive
              ? "text-primary text-lg font-medium"
              : "text-lg font-medium text-muted-foreground transition-colors hover:text-primary"
          }
        >
          Jobs
        </NavLink>
        <NavLink
          to="post"
          className={({ isActive }) =>
            isActive
              ? "text-primary text-lg font-medium"
              : "text-lg font-medium text-muted-foreground transition-colors hover:text-primary"
          }
        >
          Post Job
        </NavLink>
        <NavLink
          to="messaging"
          className={({ isActive }) =>
            isActive
              ? "text-primary text-lg font-medium"
              : "text-lg font-medium text-muted-foreground transition-colors hover:text-primary"
          }
        >
          Messaging
        </NavLink>
        <NavLink
          to="network"
          className={({ isActive }) =>
            isActive
              ? "text-primary text-lg font-medium"
              : "text-lg font-medium text-muted-foreground transition-colors hover:text-primary"
          }
        >
          My Network
        </NavLink>
      </div>
      <div className="flex items-center space-x-2 lg:space-x-4  my-4 mx-10">
        <Avatar>
          <AvatarImage
            src={
              avatar
                ? `https://careermatch-avatar.s3.ap-southeast-2.amazonaws.com/${avatar}`
                : "https://github.com/shadcn.png"
            }
          />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>

        <NavLink
          to="profile"
          className={({ isActive }) =>
            isActive
              ? "text-primary text-lg font-medium"
              : "text-lg font-medium text-muted-foreground transition-colors hover:text-primary"
          }
        >
          {name ? name : "Anonymous"}
        </NavLink>

        <AlertDialog>
          <AlertDialogTrigger asChild>
            <Button variant="outline">Log Out</Button>
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Confirm Logout</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to log out? Please make sure you have
                saved all your work before signing out. Once logged out, you
                will need to enter your credentials to access your account
                again.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={handleLogout}
                disabled={status === "pending"}
              >
                Logout
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
  );
};

export default MainNav;
