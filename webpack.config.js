const webpack = require("webpack");

module.exports = {
    entry: __dirname + "/client/index.tsx",
    output: {
        filename: "bundle.js",
        path: __dirname + "/pandas_interactive_html",
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js"],
    },
    module: {
        rules: [
            { test: /\.tsx?$/, loader: "ts-loader" },
            { test: /\.css$/, use: ["style-loader", "css-loader"] },
            { test: /\.scss$/, use: ["style-loader", "css-loader", "sass-loader"] },
        ],
    },
    plugins: [
        new webpack.DefinePlugin({
            "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV),
        }),
    ],
};
