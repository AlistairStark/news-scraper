import { Chip } from "@mui/material";
import Paper from "@mui/material/Paper";
import React, { useState } from "react";
import { ApiRoutes, SearchLocations } from "../../types";
import { HeaderSmall, Button, ScrollableView } from "../../ui-library";
import Grid from "@mui/material/Grid";
import { AiFillDelete } from "react-icons/ai";
import Tooltip from "@mui/material/Tooltip";
import { axios } from "../../services";
import { AddUrlForm, ChipText, NewUrlForm } from "./components";

type Props = {
  urls: SearchLocations[];
  searchId: number;
  width: number;
};

export const SearchUrlPanel: React.FC<Props> = ({ urls, searchId, width }) => {
  const [displayUrls, setDisplayUrls] = useState<SearchLocations[]>(urls);
  const [curId, setCurId] = useState(searchId);
  const [pendingDeleteUrls, setPendingDeleteUrls] = useState<{
    [key: number]: boolean;
  }>({});
  if (curId !== searchId) {
    setCurId(searchId);
    setDisplayUrls(urls);
  }

  const handleClick = (id: number) => {
    if (pendingDeleteUrls[id]) {
      delete pendingDeleteUrls[id];
    } else {
      pendingDeleteUrls[id] = true;
    }
    setPendingDeleteUrls({ ...pendingDeleteUrls });
  };

  const handleAddTerm = async (data: NewUrlForm) => {
    try {
      const res = await axios.post<SearchLocations[]>(
        ApiRoutes.SearchLocations,
        {
          locations: [data],
          search_id: searchId,
        }
      );
      const newUrls = displayUrls.concat(res.data);
      setDisplayUrls(newUrls);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteUrls = async () => {
    try {
      const ids = Object.keys(pendingDeleteUrls).join(",");
      const params = {
        search_id: searchId,
        ids,
      };
      await axios.delete(ApiRoutes.SearchLocations, { params });
      const filteredTerms = displayUrls.filter(
        (url) => !pendingDeleteUrls[url.id]
      );
      setDisplayUrls(filteredTerms);
      setPendingDeleteUrls({});
    } catch (err) {
      console.error(err);
    }
  };

  const sx =
    width > 900
      ? {}
      : {
          margin: "10px 0",
          overflow: "scroll",
        };

  return (
    <Paper
      sx={{
        p: 0.5,
        m: "20px 0",
      }}
    >
      <HeaderSmall style={{ textAlign: "center" }}>Search Urls</HeaderSmall>
      <Grid container spacing={0}>
        <Grid item sm={4} sx={{ justifyContent: "left" }}>
          <AddUrlForm onSubmit={handleAddTerm} />
        </Grid>
        <Grid item sm={8} sx={sx}>
          <ScrollableView>
            {displayUrls.map((url) => (
              <Chip
                key={url.id}
                label={<ChipText name={url.name} url={url.url} />}
                variant={pendingDeleteUrls[url.id] ? "filled" : "outlined"}
                sx={{ width: "90%", height: "100%", m: "0 2px 5px" }}
                onClick={() => handleClick(url.id)}
              />
            ))}
          </ScrollableView>
          <div>
            {Object.keys(pendingDeleteUrls).length > 0 && (
              <Tooltip title="Delete">
                <Button variant="outlined" color="error" onClick={deleteUrls}>
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
