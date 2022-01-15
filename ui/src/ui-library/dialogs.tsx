import { CloseButton } from "./buttons";
import { Dialog } from "@mui/material";
import React from "react";
import styled from "styled-components";

const DialogWrapper = styled.div`
  padding: 40px;
  border-radius: 2px;
`;

const FullDialogWrapper = styled.div`
  padding: 40px;
  border-radius: 2px;
  display: flex;
  align-items: center;
`;

type StandardDialogProps = {
  open: boolean;
  onClose: () => void;
};

export const StandardDialog: React.FC<StandardDialogProps> = ({
  open,
  onClose,
  children,
}) => (
  <Dialog open={open} onClose={onClose}>
    <CloseButton onClick={onClose} />
    <DialogWrapper>{children}</DialogWrapper>
  </Dialog>
);

export const FullScreenDialog: React.FC<StandardDialogProps> = ({
  open,
  onClose,
  children,
}) => (
  <Dialog open={open} onClose={onClose} fullScreen={true}>
    <CloseButton onClick={onClose} />
    <FullDialogWrapper>{children}</FullDialogWrapper>
  </Dialog>
);
