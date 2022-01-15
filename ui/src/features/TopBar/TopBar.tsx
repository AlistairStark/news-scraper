import React, { useState } from "react";
import { Navigate } from "react-router";
import { removeToken } from "../../services";
import { AppRoutes } from "../../types";
import { Button, TopMenuBar } from "../../ui-library";

export const TopBar: React.FC = () => {
  const [logout, setLogout] = useState(false);

  if (logout) {
    removeToken();
    return <Navigate to={AppRoutes.Login} />;
  }

  return (
    <TopMenuBar>
      <div></div>
      <Button onClick={() => setLogout(true)}>Logout</Button>
    </TopMenuBar>
  );
};
