import { Dashboard, Login } from "./features";
import { Navigate, Route, Routes } from "react-router-dom";

import { AppRoutes } from "./types";
import React from "react";
import { ReactJSXElement } from "@emotion/react/types/jsx-namespace";
import { isAuthenticated } from "./services";
import { BrowserRouter as Router } from "react-router-dom";

type ProtectedRouteProps = {
  authenticated: boolean;
  element: ReactJSXElement;
};

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  authenticated,
  element,
}) => {
  if (!authenticated) {
    return <Navigate to={AppRoutes.Login} />;
  }
  return element;
};

export const AppRouter: React.FC = () => {
  const authenticated = isAuthenticated();
  return (
    <Router>
      <Routes>
        <Route
          path={AppRoutes.Login}
          element={<Login isAuthenticated={authenticated} />}
        />
        <Route
          path={AppRoutes.Home}
          element={
            <ProtectedRoute
              authenticated={authenticated}
              element={<Dashboard />}
            />
          }
        />
      </Routes>
    </Router>
  );
};
