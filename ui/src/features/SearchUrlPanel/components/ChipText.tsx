import React from "react";
import { ExternalLink, TextSmall } from "../../../ui-library";

type Props = {
  name: string;
  url: string;
};

export const ChipText: React.FC<Props> = ({ name, url }) => (
  <div>
    <TextSmall>{name}</TextSmall>
    <ExternalLink href={url} target="_blank">
      {url}
    </ExternalLink>
  </div>
);
