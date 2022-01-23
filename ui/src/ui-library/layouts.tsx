import React from "react";
import { ReactJSXElement } from "@emotion/react/types/jsx-namespace";
import styled from "styled-components";
import { styles } from "./styles";
import { Sidebar } from "./sidebar";
import { useWindowWidth } from "../hooks";

const SingleWindowWrap = styled.div`
  height: 100vh;
  display: flex;
  overflow: scroll;
  background-color: ${styles.colors.lightGrey};
`;

const ContentWrap = styled.div<{ width: string }>`
  overflow-y: scroll;
  width: ${({ width }) => width};
`;

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
}) => {
  const width = useWindowWidth();
  const SIDEBAR = width > 900 ? 192 : 0;
  return (
    <SingleWindowWrap>
      <Sidebar>{menu}</Sidebar>
      <ContentWrap width={`${width - SIDEBAR}px`}>
        <TopBar>{topbar}</TopBar>
        {children}
      </ContentWrap>
    </SingleWindowWrap>
  );
};

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
  margin: 0 auto;
  border-radius: 3px;
  box-shadow: 0 0 8px ${styles.colors.black};
  padding: 10px 0;
  @media (min-width: 600px) {
    width: 400px;
    min-width: 400px;
  }
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
  @media (min-width: 600px) {
    display: flex;
    justify-content: ${(p) => p.justifyContent};
    margin-left: 60px;
  }
`;

export const ScrollableView = styled.div`
  max-height: 300px;
  overflow-y: scroll;
  margin: 0 10px 10px 0;
`;

export const MarginBottom = styled.div`
  margin-bottom: 5px;
`;

export const ButtonWrap = styled.div`
  width: 100%;
`;
