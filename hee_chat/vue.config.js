module.exports = {
  pages: {
    top: {
      entry: 'src/pages/top/main.js', // エントリーポイントとなるjs
      template: 'public/index.html', // テンプレートのHTML
      filename: 'index.html', // build時に出力されるファイル名
    },
    talks: {
      entry: 'src/pages/talks/main.js',
      template: 'public/talks.html',
      filename: 'talks.html',
    },
  },
};
