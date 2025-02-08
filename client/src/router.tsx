import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import TermsOfService from "./pages/TermsOfService";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import JobList from "./pages/JobList";
import MainLayout from "./pages/MainLayout";
import JobDetail from "./pages/JobDetail";
import Profile from "./pages/Profile";
import ProtectedRoute from "./pages/SignIn/ProtectedRoute";
import HomePage from "./pages/HomePage";
import JobPost from "./pages/JobPost";
import ProfileInfo from "./pages/ProfileInfo";
import ProfileFavorites from "./pages/ProfileFavorites";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <SignIn /> },
      { path: "signUp", element: <SignUp /> },
    ],
  },
  {
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      { path: "jobs", element: <JobList /> },
      { path: "jobs/:id", element: <JobDetail /> },
      {
        path: "profile",
        element: <Profile />,
        children: [
          { index: true, element: <ProfileInfo /> },
          { path: "favorites", element: <ProfileFavorites /> },
        ],
      },
      { path: "homePage", element: <HomePage /> },
      { path: "post", element: <JobPost /> },
    ],
  },
  { path: "/terms-of-service", element: <TermsOfService /> },
  { path: "/privacy-policy", element: <PrivacyPolicy /> },
]);

export default router;
