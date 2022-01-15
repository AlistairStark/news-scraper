import { CircularProgress, Dialog } from "@mui/material";

import React from "react";
import styled from "styled-components";

export const FullscreenLoader: React.FC = () => (
  <Dialog
    open={true}
    style={{
      width: "200px",
      marginLeft: "40%",
      backgroundColor: "transparent",
    }}
    title="Loading"
    PaperProps={{ style: { background: "transparent", boxShadow: "none" } }}
  >
    <CircularProgress />
  </Dialog>
);

const LoaderWrap = styled.div`
  padding-top: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
`;

type LoaderProps = {
  padding: string;
};

export const Loader: React.FC<LoaderProps> = ({ padding }) => (
  <LoaderWrap style={{ padding }}>
    <CircularProgress />
  </LoaderWrap>
);
