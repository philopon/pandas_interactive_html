import "react-table/react-table.css";
import "./main.scss";

import * as React from "react";
import * as ReactDOM from "react-dom";

import * as ReactTable from "react-table";

interface TableData {
    columns: Array<{ name: string; type: "string" | "number" | "image" | "other" }>;
    data: any[][];
}

interface AppProps extends TableData {}

interface AppState {}

function sortNumber(a: number, b: number): number {
    return Number(a) - Number(b);
}

function sortString(a: string, b: string): number {
    const sa = String(a).toLowerCase();
    const sb = String(b).toLowerCase();
    if (sa > sb) {
        return 1;
    }
    if (sa < sb) {
        return -1;
    }
    return 0;
}

function renderImage({ value }: { value: string }) {
    return (
        <div className="image-cell cell">
            <img src={value} />
        </div>
    );
}

function renderNormal({ value }: { value: any }) {
    return (
        <div className="cell">
            <div>{value}</div>
        </div>
    );
}

class App extends React.Component<AppProps, AppState> {
    constructor(props: AppProps) {
        super(props);
        this.state = {};
    }

    render() {
        const columns = this.props.columns.map<ReactTable.Column>(({ name, type }, index) => ({
            Header: name,
            id: index.toString(),
            accessor: (d: TableData["data"]) => d[index],
            sortable: type === "number" || type === "string",
            filterable: type === "number" || type === "string",
            sortMethod: type === "number" ? sortNumber : sortString,
            Cell: type === "image" ? renderImage : renderNormal,
        }));

        return (
            <div className="content-wrapper">
                <ReactTable.default
                    style={{ height: "100%" }}
                    defaultPageSize={100}
                    filterable
                    data={this.props.data}
                    columns={columns}
                />
            </div>
        );
    }
}

const columnsElement = document.querySelector(".table-columns");
const dataElement = document.querySelector(".table-data");

if (columnsElement !== null && dataElement !== null) {
    const columns: TableData["columns"] = JSON.parse(columnsElement.innerHTML);
    const data: TableData["data"] = JSON.parse(dataElement.innerHTML);

    ReactDOM.render(<App columns={columns} data={data} />, document.querySelector(".mount-point"));
}
