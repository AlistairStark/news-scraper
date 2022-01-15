import Paper from "@mui/material/Paper";
import Tooltip from "@mui/material/Tooltip";
import React, { useState } from "react";
import { Search } from "../../../types";
import {
  Text,
  HeaderSmall,
  Button,
  StandardDialog,
  MediumHeader,
  TextSmall,
} from "../../../ui-library";
import { AiOutlineEdit, AiFillDelete } from "react-icons/ai";
import { FcCheckmark, FcCancel } from "react-icons/fc";

type Props = {
  search: Search;
  onUpdate: () => void;
  onDelete: () => void;
};

export const UpdateSearch: React.FC<Props> = ({
  search,
  onUpdate,
  onDelete,
}) => {
  const [confirmDelete, setConfirmDelete] = useState(false);
  return (
    <Paper style={{ textAlign: "left", padding: "5px 20px" }}>
      <StandardDialog
        open={confirmDelete}
        onClose={() => setConfirmDelete(false)}
      >
        <MediumHeader>
          Are you sure you want to delete this search?
        </MediumHeader>
        <Button
          variant="outlined"
          color="success"
          style={{ marginRight: "5px" }}
          onClick={onDelete}
        >
          <FcCheckmark size={20} />
        </Button>
        <Button
          variant="outlined"
          color="error"
          onClick={() => setConfirmDelete(false)}
        >
          <FcCancel size={20} />
        </Button>
      </StandardDialog>
      <HeaderSmall>{search.name}</HeaderSmall>
      <Text>{search.description}</Text>
      {search.is_rss && <TextSmall>RSS mode enabled</TextSmall>}
      <Tooltip title="Edit">
        <Button
          onClick={onUpdate}
          variant="outlined"
          style={{ marginRight: "5px" }}
        >
          <AiOutlineEdit />
        </Button>
      </Tooltip>
      <Tooltip title="Delete">
        <Button
          variant="outlined"
          color="error"
          onClick={() => setConfirmDelete(true)}
        >
          <AiFillDelete />
        </Button>
      </Tooltip>
    </Paper>
  );
};
