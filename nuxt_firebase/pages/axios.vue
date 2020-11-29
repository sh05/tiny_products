<template>
  <section class="container">
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
  </section>
</template>

<style>
ul {
  margin: 0px 10px;
  background-color: alicebule;
}
li {
  padding: 10px;
  font-size: 16px;
}
.container {
  padding: 5px 10px;
}
h1 {
  font-size: 60px;
  color: #345980;
}
p {
  padding-top: 5px;
  font-size: 20px;
}
div {
  font-size: 14px;
}
</style>

<script>
import firebase from "firebase";

export default {
  data: function() {
    return {
      title: "Auth",
      message: "This is message",
    };
  },
  created: function() {
    // Your web app's Firebase configuration
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    var firebaseConfig = {
      apiKey: process.env.API_KEY,
      authDomain: process.env.AUTH_DOMAIN,
      databaseURL: process.env.DATABASE_URL,
      projectId: process.env.PROJECT_ID,
      storageBucket: process.env.STORAGE_BUCKET,
      messagingSenderId: process.env.MESSAGINGSENDER_ID,
      appId: process.env.APP_ID,
      measurementId: process.env.MEASUREMENT_ID
    };
    if (!firebase.apps.length) {
      // Initialize Firebase
      firebase.initializeApp(firebaseConfig);
    }

    var provider = new firebase.auth.GoogleAuthProvider();
    var self = this;
    firebase.auth().signInWithPopup(provider)
      .then(function(result) {
        self.message = result.user.displayName + ", " + result.user.email;
      }).catch(function(error) {
        console.log(error);
      });
  },
}
</script>

