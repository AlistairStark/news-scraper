import React, { useState } from "react";

import { DashboardSidebarWrap } from "../../ui-library";
import { Loader } from "../../ui-library/loader";
import { AddOrEdit, ApiRoutes, SearchMenu } from "../../types";
import { TopBar } from "../TopBar";
import { AddEditSearch } from "../AddEditSearch";
import { DashboardContent } from "./DashboardContent";
import { DashboardMenu } from "./DashboardMenu";
import { useApi, useWindowWidth } from "../../hooks";

export const Dashboard: React.FC = () => {
  const [selectedId, setSelectedId] = useState<number | undefined>();
  const [addSearch, setAddSearch] = useState<AddOrEdit | undefined>();
  const width = useWindowWidth();
  const {
    data: menuData,
    loading,
    refetch: refetchMenu,
  } = useApi<SearchMenu[]>(ApiRoutes.SearchAll);

  const onAddNewSearch = () => {
    setAddSearch(undefined);
    refetchMenu();
  };

  const onDelete = () => {
    setSelectedId(undefined);
    refetchMenu();
  };

  const selectNew = (id: number) => {
    setSelectedId(id);
  };

  return (
    <DashboardSidebarWrap
      menu={
        <DashboardMenu
          elements={menuData}
          selectedId={selectedId}
          onSelect={selectNew}
          addSearch={() => setAddSearch(AddOrEdit.Add)}
        />
      }
      topbar={<TopBar />}
    >
      {!loading && addSearch && (
        <AddEditSearch
          type={addSearch}
          open={!!addSearch}
          onSuccess={onAddNewSearch}
          onClose={() => setAddSearch(undefined)}
        />
      )}
      {loading && <Loader padding={"300px"} />}
      {selectedId && (
        <DashboardContent
          id={selectedId}
          width={width}
          refetchMenu={refetchMenu}
          onDelete={onDelete}
        />
      )}
    </DashboardSidebarWrap>
  );
};
