module.exports = {
  devServer: {
    proxy: {
      '/app': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
};