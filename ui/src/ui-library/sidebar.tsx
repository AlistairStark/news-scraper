import React, { useState } from "react";
import styled from "styled-components";
import { SiAircanada } from "react-icons/si";
import { styles } from "./styles";
import { useWindowWidth } from "../hooks";
import { SwipeableDrawer } from "@mui/material";
import { HiMenuAlt2 } from "react-icons/hi";
import { TransparentButton } from "./buttons";

const Title = styled.div`
  color: ${styles.colors.white};
  text-transform: uppercase;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-bottom: 20px;
`;

const Bar = styled.div`
  padding: 20px 10px;
  height: 100%;
  min-height: 100vh;
  width: 10vw;
  min-width: 180px;
  max-width: 250px;
  background-color: ${styles.colors.darkBlue};
`;

const HamburgerWrap = styled.span`
  position: absolute;
  top: 0;
  left: 0;
  padding: 20px;
`;

const MobileMenuWrap = styled.div`
  padding: 20px;
`;

const DrawerTitle: React.FC = () => (
  <Title>
    <span>Daily Ops</span>
    <SiAircanada size="2em" color={styles.colors.canadaRed} />
  </Title>
);

const MobileDrawer: React.FC = ({ children }) => {
  const [open, setOpen] = useState(false);
  return (
    <>
      <HamburgerWrap>
        <TransparentButton onClick={() => setOpen(true)}>
          <HiMenuAlt2 size="2em" />
        </TransparentButton>
      </HamburgerWrap>
      <SwipeableDrawer
        PaperProps={{
          sx: {
            backgroundColor: styles.colors.darkBlue,
          },
        }}
        open={open}
        onOpen={() => setOpen(true)}
        onClose={() => setOpen(false)}
      >
        <MobileMenuWrap>
          <DrawerTitle />
          <div>{children}</div>
        </MobileMenuWrap>
      </SwipeableDrawer>
    </>
  );
};

const FullScreenDrawer: React.FC = ({ children }) => (
  <Bar>
    <DrawerTitle />
    <div>{children}</div>
  </Bar>
);

export const Sidebar: React.FC = ({ children }) => {
  const FULLSCREEN = 900;
  const [fullScreen, setFullScreen] = useState(false);
  const width = useWindowWidth();
  if (width > FULLSCREEN && !fullScreen) {
    setFullScreen(true);
  } else if (width <= FULLSCREEN && fullScreen) {
    setFullScreen(false);
  }
  return fullScreen ? (
    <FullScreenDrawer>{children}</FullScreenDrawer>
  ) : (
    <MobileDrawer>{children}</MobileDrawer>
  );
};
