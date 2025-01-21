const { DefinePlugin } = require('webpack');

module.exports = {
  configureWebpack: {
    plugins: [
      new DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('development'),
      }),
    ],
  },
  
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
};
