import React from "react";
import { ReactJSXElement } from "@emotion/react/types/jsx-namespace";
import { SiAircanada } from "react-icons/si";
import styled from "styled-components";
import { styles } from "./styles";

const SingleWindowWrap = styled.div`
  height: 100vh;
  min-width: 100vw;
  display: flex;
  overflow: scroll;
  background-color: ${styles.colors.lightGrey};
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

const ContentWrap = styled.div`
  width: 86vw;
  overflow-y: scroll;
`;

const Title = styled.div`
  color: ${styles.colors.white};
  text-transform: uppercase;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-bottom: 20px;
`;

export const Sidebar: React.FC = ({ children }) => (
  <Bar>
    <Title>
      <span>Daily Ops</span>
      <SiAircanada size="2em" color={styles.colors.canadaRed} />
    </Title>
    <div>{children}</div>
  </Bar>
);

const TopBar = styled.div`
  width: 100%;
`;

type Props = {
  menu: ReactJSXElement;
  topbar: ReactJSXElement;
};

export const DashboardSidebarWrap: React.FC<Props> = ({
  menu,
  topbar,
  children,
}) => (
  <SingleWindowWrap>
    <Sidebar>{menu}</Sidebar>
    <ContentWrap>
      <TopBar>{topbar}</TopBar>
      {children}
    </ContentWrap>
  </SingleWindowWrap>
);

export const MenuSeparator = styled.div`
  position: relative;
  text-transform: none;
  &:after {
    content: "";
    position: absolute;
    height: 1px;
    width: 40%;
    left: 50%;
    opacity: 0.4;
    bottom: 0;
    transform: translateX(-50%);
    background-color: ${styles.colors.white};
  }
`;

export const TopMenuBar = styled.div`
  height: 50px;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 0 10px ${styles.colors.darkGrey};
`;

export const LoginPageWrap = styled.div`
  background-color: ${styles.colors.darkBlue};
  min-height: 100vh;
  padding-top: 50px;
`;

export const LoginInner = styled.div`
  background-color: ${styles.colors.lightGrey};
  width: 400px;
  min-width: 400px;
  margin: 0 auto;
  border-radius: 3px;
  box-shadow: 0 0 8px ${styles.colors.black};
  padding: 10px 0;
`;

export const LoginWrap: React.FC = ({ children }) => (
  <LoginPageWrap>
    <LoginInner>{children}</LoginInner>
  </LoginPageWrap>
);

export const PaddingWrap = styled.div`
  padding: 20px 20px;
`;

export const FlexWrap = styled.div<{
  justifyContent: "left" | "center" | "space-around" | "space-between";
}>`
  display: flex;
  justify-content: ${(p) => p.justifyContent};
  margin-left: 60px;
`;

export const ScrollableView = styled.div`
  max-height: 300px;
  overflow-y: scroll;
  margin: 0 10px 10px 0;
`;

export const MarginBottom = styled.div`
  margin-bottom: 5px;
`;
