import { useNavigate } from "react-router-dom";
import { ReactNode, useEffect, useState } from "react";
import { useUser } from "./useUser";
import toast from "react-hot-toast";

interface ProtectedRouteProps {
  children: ReactNode;
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate();
  const [checkingAuth, setCheckingAuth] = useState(true);
  
  const { isLoading, fetchStatus, isAuthenticated, error } = useUser();

  useEffect(() => {
    // 调试信息
    console.log("Auth state:", { 
      isAuthenticated, 
      isLoading, 
      fetchStatus, 
      hasToken: Boolean(localStorage.getItem("access_token"))
    });
    
    // 如果验证结束且未认证
    if (!isAuthenticated && !isLoading && fetchStatus !== "fetching") {
      console.log("Not authenticated, redirecting to login");
      // 清除所有token
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      
      toast.error("Please login to access this page");
      navigate("/");
    }
    
    // 验证过程结束
    if (!isLoading && fetchStatus !== "fetching") {
      setCheckingAuth(false);
    }
  }, [isAuthenticated, isLoading, fetchStatus, navigate, error]);

  // 显示加载中状态
  if (isLoading || checkingAuth) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // 认证成功
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // 认证失败，显示加载中状态，等待重定向
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900"></div>
    </div>
  );
}

export default ProtectedRoute;
