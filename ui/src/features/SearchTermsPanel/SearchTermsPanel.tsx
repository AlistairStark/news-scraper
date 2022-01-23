import { Chip } from "@mui/material";
import Paper from "@mui/material/Paper";
import React, { useState } from "react";
import { ApiRoutes, SearchTerms } from "../../types";
import { HeaderSmall, Button, MarginBottom } from "../../ui-library";
import { AddTermForm, NewTermForm } from "./components";
import Grid from "@mui/material/Grid";
import { AiFillDelete } from "react-icons/ai";
import Tooltip from "@mui/material/Tooltip";
import { axios } from "../../services";

type Props = {
  terms: SearchTerms[];
  searchId: number;
  width: number;
};

export const SearchTermsPanel: React.FC<Props> = ({
  terms,
  searchId,
  width,
}) => {
  const [displayTerms, setDisplayTerms] = useState<SearchTerms[]>(terms);
  const [curId, setCurId] = useState(searchId);
  const [pendingDeleteTerms, setPendingDeleteTerms] = useState<{
    [key: number]: boolean;
  }>({});

  if (curId !== searchId) {
    setCurId(searchId);
    setDisplayTerms(terms);
  }

  const handleClick = (id: number) => {
    if (pendingDeleteTerms[id]) {
      delete pendingDeleteTerms[id];
    } else {
      pendingDeleteTerms[id] = true;
    }
    setPendingDeleteTerms({ ...pendingDeleteTerms });
  };

  const handleAddTerm = async (data: NewTermForm) => {
    try {
      const res = await axios.post<SearchTerms[]>(ApiRoutes.SearchTerms, {
        terms: [data.term],
        search_id: searchId,
      });
      const newTerms = displayTerms.concat(res.data);
      setDisplayTerms(newTerms);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteTerms = async () => {
    try {
      const ids = Object.keys(pendingDeleteTerms).join(",");
      const params = {
        search_id: searchId,
        ids,
      };
      await axios.delete(ApiRoutes.SearchTerms, { params });
      const filteredTerms = displayTerms.filter(
        (term) => !pendingDeleteTerms[term.id]
      );
      setDisplayTerms(filteredTerms);
      setPendingDeleteTerms({});
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Paper
      sx={{
        p: 0.5,
        m: "20px 0",
      }}
    >
      <HeaderSmall style={{ textAlign: "center" }}>Search Terms</HeaderSmall>
      <Grid
        container
        spacing={2}
        sx={{ justifyContent: width > 900 ? "left" : "center" }}
      >
        <Grid
          item
          sm={3}
          sx={{ justifyContent: width > 900 ? "left" : "center" }}
        >
          <AddTermForm onSubmit={handleAddTerm} />
        </Grid>
        <Grid item sm={9}>
          <MarginBottom>
            {displayTerms.map((term) => (
              <Chip
                key={term.id}
                label={term.term}
                variant={pendingDeleteTerms[term.id] ? "filled" : "outlined"}
                onClick={() => handleClick(term.id)}
              />
            ))}
          </MarginBottom>
          <div>
            {Object.keys(pendingDeleteTerms).length > 0 && (
              <Tooltip title="Delete">
                <Button variant="outlined" color="error" onClick={deleteTerms}>
                  <AiFillDelete />
                </Button>
              </Tooltip>
            )}
          </div>
        </Grid>
      </Grid>
    </Paper>
  );
};
