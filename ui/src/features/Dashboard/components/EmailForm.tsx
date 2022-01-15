import React from "react";

type Props = {
  ids: number[];
  searchId: number;
  close: () => void;
};

export const EmailForm: React.FC<Props> = ({ ids, searchId, close }) => {
  const text = "<h1>THIS IS A TEST</h1>";
  const type = "text/html";
  const blob = new Blob([text], { type });
  const data = [new ClipboardItem({ "text/html": blob as any })];

  navigator.clipboard.write(data).then(
    function () {
      console.log("Async: Copying to clipboard was successful!");
    },
    function (err) {
      console.error("Async: Could not copy text: ", err);
    }
  );

  return <>Copied to clipboard!</>;
};
