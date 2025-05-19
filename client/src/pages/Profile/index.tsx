import { buttonVariants } from "@/components/ui/button";
import { NavLink, Outlet } from "react-router-dom";

export default function Profile() {
  const role = localStorage.getItem("role"); // ✅ 从 localStorage 读取角色

  return (
    <>
      {role === "candidate" && (
        <div className="flex justify-center pt-10 bg-gray-50">
          <div className="inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground">
            <NavLink
              to="/profile"
              end
              className={({ isActive }) =>
                isActive
                  ? buttonVariants({ variant: "outline" })
                  : buttonVariants({ variant: "ghost" })
              }
            >
              User Info
            </NavLink>
            <NavLink
              to="favorites"
              className={({ isActive }) =>
                isActive
                  ? buttonVariants({ variant: "outline" })
                  : buttonVariants({ variant: "ghost" })
              }
            >
              Favorite Jobs
            </NavLink>
            <NavLink
              to="history"
              className={({ isActive }) =>
                isActive
                  ? buttonVariants({ variant: "outline" })
                  : buttonVariants({ variant: "ghost" })
              }
            >
              History
            </NavLink>
          </div>
        </div>
      )}

      {/* 公共组件 */}
      <Outlet />
    </>
  );
}
