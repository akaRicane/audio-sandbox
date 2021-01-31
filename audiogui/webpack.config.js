module.exports = {
  entry: {
      main: "./project/static/scripts/jsx/main.js",
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
              use: ["style-loader", "css-loader"],
          },
      ],
  },
  output: {
      path: __dirname + "/project/static/scripts/js",
      filename: "[name].js",
  },
};
