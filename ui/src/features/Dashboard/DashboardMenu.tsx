import { Button, MenuSeparator } from "../../ui-library";

import { AiOutlinePlus } from "react-icons/ai";
import React from "react";
import { SearchMenu } from "../../types";

type Props = {
  elements: SearchMenu[] | undefined;
  selectedId: number | undefined;
  onSelect: (index: number) => void;
  addSearch: () => void;
};

export const DashboardMenu: React.FC<Props> = ({
  elements,
  selectedId,
  onSelect,
  addSearch,
}) => {
  return (
    <div>
      {elements &&
        elements.map((elem) => {
          const disabled = selectedId === elem.id;
          const style = { width: "100%", color: "white" };
          if (disabled) {
            style.color = "grey";
          }
          return (
            <MenuSeparator key={`${elem.id}-${elem.name}`}>
              <Button
                disabled={selectedId === elem.id}
                style={style}
                onClick={() => onSelect(elem.id)}
              >
                {elem.name}
              </Button>
            </MenuSeparator>
          );
        })}
      <Button onClick={addSearch} style={{ width: "100%", color: "white" }}>
        Add New Search <AiOutlinePlus />
      </Button>
    </div>
  );
};
