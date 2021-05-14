import React from "react";
import { HDoc } from "../App";
import styles from "./Preview.module.css";

export function Preview({ table }: { table: HDoc }) {
  return (
    <div className={styles.preview}>
      {table.map((el, i) => {
        if (el.type === "text") {
          return (
            <div key={i}>
              <p>{el.data}</p>
            </div>
          );
        } else if (el.type === "table") {
          return (
            <table
              key={i}
              style={{
                borderCollapse: "collapse",
                // border: "1px solid black",
              }}
            >
              <tbody>
                {el.data.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td style={{ border: "1px solid black" }} key={cellIndex}>
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          );
        }
        return null;
      })}
    </div>
  );
}