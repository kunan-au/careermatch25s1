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
    // Debug information
    console.log("Auth state:", { 
      isAuthenticated, 
      isLoading, 
      fetchStatus, 
      hasToken: Boolean(localStorage.getItem("access_token"))
    });
    
    // If validation ended and not authenticated
    if (!isAuthenticated && !isLoading && fetchStatus !== "fetching") {
      console.log("Not authenticated, redirecting to login");
      // Clear all tokens
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      
      toast.error("Please login to access this page");
      navigate("/");
    }
    
    // Validation process ended
    if (!isLoading && fetchStatus !== "fetching") {
      setCheckingAuth(false);
    }
  }, [isAuthenticated, isLoading, fetchStatus, navigate, error]);

  // Show loading state
  if (isLoading || checkingAuth) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // Authenticated successfully
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // Authenticated failed, show loading state, waiting for redirection
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900"></div>
    </div>
  );
}

export default ProtectedRoute;
