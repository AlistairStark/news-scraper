import { ResultsGrid, UpdateSearch } from "./components";
import React, { useState } from "react";

import { PaddingWrap } from "../../ui-library";
import Grid from "@mui/material/Grid";
import { Loader } from "../../ui-library/loader";
import { AddOrEdit, ApiRoutes, Search } from "../../types";
import { AddEditSearch } from "../AddEditSearch";
import { axios } from "../../services";
import { SearchTermsPanel } from "../SearchTermsPanel";
import { useApi } from "../../hooks";
import { SearchUrlPanel } from "..";

type Props = {
  id: number | undefined;
  refetchMenu: () => void;
  onDelete: () => void;
};

export const DashboardContent: React.FC<Props> = ({
  id,
  refetchMenu,
  onDelete,
}) => {
  const [addSearch, setAddSearch] = useState<AddOrEdit | undefined>(undefined);
  const {
    data,
    loading,
    refetch: refetchSearch,
  } = useApi<Search>(ApiRoutes.Search, {
    params: { search_id: id },
  });

  const editSuccess = async () => {
    setAddSearch(undefined);
    await refetchSearch();
    await refetchMenu();
  };

  const editSearch = () => {
    setAddSearch(AddOrEdit.Edit);
  };

  const deleteSearch = async () => {
    if (!data) {
      return;
    }
    const id = data.id;
    try {
      await axios.delete(ApiRoutes.Search, { params: { id } });
      onDelete();
    } catch (err) {
      console.error(err);
    }
  };

  const getCols = (): number => {
    if (data?.is_rss) {
      return 12;
    }
    return window.innerWidth < 1300 ? 12 : 6;
  };

  const cols = getCols();

  return (
    <>
      {loading && <Loader padding={"300px"} />}
      {!loading && data && addSearch && (
        <AddEditSearch
          type={addSearch}
          open={!!addSearch}
          selected={data}
          onSuccess={editSuccess}
          onClose={() => setAddSearch(undefined)}
        />
      )}
      {!loading && data && (
        <PaddingWrap>
          <UpdateSearch
            search={data}
            onUpdate={editSearch}
            onDelete={deleteSearch}
          />
          <Grid container spacing={cols === 12 ? 0 : 2}>
            <Grid item xs={cols}>
              <SearchUrlPanel searchId={data.id} urls={data.search_locations} />
            </Grid>
            {!data.is_rss && (
              <Grid item xs={cols}>
                <SearchTermsPanel
                  searchId={data.id}
                  terms={data.search_terms}
                />
              </Grid>
            )}
          </Grid>
          <ResultsGrid searchId={data.id} />
        </PaddingWrap>
      )}
    </>
  );
};
