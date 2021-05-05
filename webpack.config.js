var webpack = require('webpack');
module.exports = {
  entry: {
    main: "./audiogui/project/static/scripts/jsx/index.js",
  },
  output: {
    path: __dirname + "/audiogui/project/static/scripts/js",
    filename: "index.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: "babel-loader",
      },
      {
        test: /\.(svg|png|jpg|jpeg|gif)$/,
        loader: "file-loader",

        options: {
          name: "[name].[ext]",
          outputPath: "../../static/dist",
        },
      },
      {
        test: /\.css$/i,
        exclude: /node_modules/,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
    ],
  },
};
