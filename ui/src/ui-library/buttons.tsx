import { AiOutlineClose } from "react-icons/ai";
import MatButton from "@mui/material/Button";
import styled from "styled-components";
import { styles } from "./styles";

export const Button = MatButton;

const CloseButtonWrap = styled.button`
  background-color: transparent;
  border: none;
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0;
  opacity: 0.2;
  fill: ${styles.colors.darkGrey};
  &:hover {
    cursor: pointer;
    opacity: 0.5;
  }
  svg {
    height: 18px;
    width: 18px;
  }
`;

interface CloseButtonProps {
  onClick: () => void;
}

export const CloseButton: React.FC<CloseButtonProps> = ({ onClick }) => (
  <CloseButtonWrap onClick={onClick}>
    <AiOutlineClose />
  </CloseButtonWrap>
);
