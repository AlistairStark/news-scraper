import React from "react";
import "./App.css";
import { AppRouter } from "./routes";
import { initAxios } from "./services";

const App: React.FC = () => {
  initAxios();
  return (
    <div className="App">
      <AppRouter />
    </div>
  );
};

export default App;
