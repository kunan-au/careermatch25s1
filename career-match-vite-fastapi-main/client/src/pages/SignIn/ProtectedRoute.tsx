import { useNavigate } from "react-router-dom";
import { ReactNode, useEffect } from "react";
import { useUser } from "./useUser";

interface ProtectedRouteProps {
  children: ReactNode;
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate();

  const { isLoading, fetchStatus, isAuthenticated } = useUser();

  useEffect(() => {
    if (!isAuthenticated && !isLoading && fetchStatus !== "fetching") {
      navigate("/");
    }
  }, [isAuthenticated, isLoading, fetchStatus, navigate]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <>{children}</>;
  }

  return null;
}

export default ProtectedRoute;
