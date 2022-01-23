import Paper from "@mui/material/Paper";
import React, { useState } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Card from "@mui/material/Card";
import {
  CircularProgress,
  FormControlLabel,
  Switch,
  Tooltip,
} from "@mui/material";
import {
  Button,
  FlexWrap,
  FullScreenDialog,
  PaddingWrap,
  TextSmall,
  HeaderSmall,
  ButtonWrap,
} from "../../../ui-library";
import { axios } from "../../../services";
import { ApiRoutes } from "../../../types";
import Checkbox from "@mui/material/Checkbox";
import FileSaver from "file-saver";
import { copyTable, makeTable } from "../../../services/copyTable";
import { toast } from "react-toastify";

export type ScrapeResults = {
  id: number;
  agency: string;
  title: string;
  link: string;
  deleted: boolean;
  updated_at: string;
};

type Props = {
  searchId: number;
  width: number;
};

export const ResultsGrid: React.FC<Props> = ({ searchId, width }) => {
  const [rows, setRows] = useState<ScrapeResults[]>([]);
  const [loading, setLoading] = useState(false);
  const [showHTML, setHTML] = useState<string>("");
  const [excluded, setExcluded] = useState<Set<string>>(new Set());
  const [includePrevious, setIncludePrevious] = useState(false);

  const doSearch = async () => {
    setLoading(true);
    const params = {
      search_id: searchId,
      include_previous: includePrevious,
    };
    try {
      const res = await axios.get<{ links: ScrapeResults[] }>(
        ApiRoutes.Scrape,
        { params }
      );
      if (res?.data?.links) {
        setRows(res.data.links);
      }
    } catch (err: any) {
      console.log("err: ", err.response);
    }
    setLoading(false);
  };

  const downloadResults = async () => {
    const csvString = `"Agency","Title","Link" \n${rows
      .filter((r) => !excluded.has(r.link))
      .map((r) => `"${r.agency}","${r.title}","${r.link}"\n`)
      .join("")}`;
    const csv = new Blob([csvString], { type: "text/csv;charset=utf-8;" });
    FileSaver.saveAs(csv, "results.csv");
  };

  const handleExcludedCheck = (link: string) => {
    if (excluded.has(link)) {
      excluded.delete(link);
    } else {
      excluded.add(link);
    }
    setExcluded(new Set(excluded));
  };

  const filterExcludedRows = (): ScrapeResults[] =>
    rows.filter((r) => !excluded.has(r.link));

  const marginBottom = width < 900 ? "5px" : 0;

  return (
    <Paper sx={{ width: "100%" }}>
      <PaddingWrap>
        <FlexWrap justifyContent="space-between">
          <ButtonWrap>
            <Button
              onClick={doSearch}
              variant="contained"
              sx={{ marginRight: "5px" }}
            >
              {loading ? (
                <CircularProgress color="inherit" size={25} />
              ) : (
                "Search"
              )}
            </Button>

            <Tooltip title="Include search results that have been seen before.">
              <FormControlLabel
                control={
                  <Switch
                    checked={includePrevious}
                    onChange={() => setIncludePrevious(!includePrevious)}
                    name="previous"
                  />
                }
                label="Include Previous"
              />
            </Tooltip>
          </ButtonWrap>
          <ButtonWrap>
            {rows.length > 0 && (
              <>
                <Button
                  onClick={() => {
                    const rows = filterExcludedRows();
                    const html = makeTable(rows);
                    setHTML(html);
                  }}
                  variant="contained"
                  sx={{ marginRight: "5px", marginBottom }}
                >
                  HTML Preview
                </Button>
                <Button
                  onClick={async () => {
                    try {
                      await copyTable(filterExcludedRows());
                      toast.success("Copied to clipboard!");
                    } catch (err) {
                      console.error(err);
                      toast.error(
                        "Error copying to clipboard. Try another browser."
                      );
                    }
                  }}
                  variant="contained"
                  sx={{ marginRight: "5px", marginBottom }}
                >
                  Copy To Clipboard
                </Button>
                <Button
                  onClick={downloadResults}
                  variant="contained"
                  sx={{ marginRight: "5px", marginBottom }}
                >
                  Download
                </Button>
              </>
            )}
          </ButtonWrap>
        </FlexWrap>
        <TextSmall>{rows.length} results</TextSmall>
      </PaddingWrap>
      <FullScreenDialog open={!!showHTML} onClose={() => setHTML("")}>
        <div
          style={{ width: "100vw" }}
          dangerouslySetInnerHTML={{ __html: showHTML }}
        />
      </FullScreenDialog>
      {width <= 900 ? (
        <>
          {rows.map((row) => {
            const styles = {
              padding: "5px",
              margin: "5px 0",
              opacity: 1,
            };
            if (excluded.has(row.link)) {
              styles["opacity"] = 0.25;
            }
            return (
              <Card sx={styles} key={row.id}>
                <HeaderSmall>{row.agency}</HeaderSmall>
                <TextSmall>{row.title}</TextSmall>
                <TextSmall>
                  <a href={row.link} rel="noreferrer" target="_blank">
                    {row.link}
                  </a>
                </TextSmall>
                <Checkbox onChange={() => handleExcludedCheck(row.link)} />
              </Card>
            );
          })}
        </>
      ) : (
        <Table sx={{ minWidth: 650 }} size="small" aria-label="Results">
          <TableHead>
            <TableRow>
              <TableCell>Agency</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Link</TableCell>
              <TableCell align="right">Exclude</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => {
              const styles = {
                opacity: 1,
                height: "100",
              };
              if (excluded.has(row.link)) {
                styles["opacity"] = 0.25;
                styles["height"] = "5px";
              }
              return (
                <TableRow
                  key={row.title}
                  sx={{
                    "&:last-child td, &:last-child th": { border: 0 },
                    ...styles,
                  }}
                >
                  <TableCell component="th" scope="row">
                    {row.agency}
                  </TableCell>
                  <TableCell>{row.title}</TableCell>
                  <TableCell>
                    <a href={row.link} rel="noreferrer" target="_blank">
                      {row.link}
                    </a>
                  </TableCell>
                  <TableCell align="right">
                    <Checkbox onChange={() => handleExcludedCheck(row.link)} />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      )}
    </Paper>
  );
};
