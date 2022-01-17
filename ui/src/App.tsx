import React from "react";
import "./App.css";
import { AppRouter } from "./routes";
import { initAxios } from "./services";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const App: React.FC = () => {
  initAxios();
  return (
    <div className="App">
      <AppRouter />
      <ToastContainer />
    </div>
  );
};

export default App;
