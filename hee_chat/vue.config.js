module.exports = {
  "pages": {
    "top": {
      "entry": "src/pages/top/main.js",
      "template": "public/index.html",
      "filename": "index.html"
    },
    "talks": {
      "entry": "src/pages/talks/main.js",
      "template": "public/talks.html",
      "filename": "talks.html"
    }
  },
  "transpileDependencies": [
    "vuetify"
  ]
}