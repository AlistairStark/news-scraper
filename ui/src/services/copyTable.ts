import { ScrapeResults } from "../features/Dashboard/components";

function headings(): string {
  return `<tr style="height:14.4pt">
  <td 
    width="61"
    nowrap
    valign="top"
    style="width:46.1pt;border:solid windowtext 1.0pt;background:#bfbfbf;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt"
  >
    <p style="margin="0";margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal">
      <b>
        <span style="color:black">
          Agency
        </span>
      </b>
    </p>
  </td>
  <td 
    width="307"
    nowrap
    valign="top"
    style="width:230.05pt;border:solid windowtext 1.0pt;background:#bfbfbf;border-left:none;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt"
  >
    <p style="margin="0";margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal">
      <b>
        <span style="color:black">
          Title
        </span>
      </b>
    </p>
  </td>
  <td 
    width="61"
    nowrap
    valign="top"
    style="width:46.1pt;border:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt;background:#bfbfbf;"
  >
    <p style="margin="0";width:326.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt">
      <b>  
        <span style="color:black">
          URL
        </span>
      </b>
    </p>
  </td>
</tr>`;
}

function generateRow(row: ScrapeResults): string {
  return `<tr style="height:14.4pt">
      <td 
        width="61"
        nowrap
        valign="top"
        style="width:46.1pt;border:solid windowtext 1.0pt;background:#bfbfbf;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt"
      >
        <p style="margin="0";margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal">
          <b>
            <span style="color:black">
              ${row.agency}
            </span>
          </b>
        </p>
      </td>
      <td 
        width="307"
        nowrap
        valign="top"
        style="width:230.05pt;border:solid windowtext 1.0pt;border-left:none;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt"
      >
        <p style="margin="0";margin-bottom:0cm;margin-bottom:.0001pt;line-height:normal">
          <span style="color:black">
          ${row.title}
          </span>
        </p>
      </td>
      <td 
        width="61"
        nowrap
        valign="top"
        style="width:46.1pt;border:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt"
      >
        <p style="margin="0";width:326.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt;height:14.4pt">
          <span style="color:black">
            <a href="${row.link}" target="_blank">${row.link}</a>
          </span>
        </p>
      </td>
    </tr>
  `;
}

export function makeTable(rows: ScrapeResults[]): string {
  return `<table 
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="0"
      style="width:602.15pt;border-collapse:collapse;"
    >
      <tbody>
        ${headings()}
        ${rows.map(generateRow)}
      </tbody>
    </table>  
  `;
}

export const copyTable = (rows: ScrapeResults[]) => {
  const text = makeTable(rows);
  const type = "text/html";
  const blob = new Blob([text.trim()], { type });
  const data = [new ClipboardItem({ "text/html": blob as any })];

  navigator.clipboard.write(data).then(
    () => {
      alert("Copied to clipboard!");
    },
    (err) => {
      alert("Could not copy text. Try another browser.");
      console.error("Async: Could not copy text: ", err);
    }
  );
};
