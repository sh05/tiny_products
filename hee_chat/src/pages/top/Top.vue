<template>
  <div id="app">
    <h1>hello</h1>
    <h1>WebSocket Chat</h1>
      <h2>Your Name: </h2>
      <input type="text" v-model="user_name" autocomplete="off"/>
      <h2>Room: </h2>
      <v-tabs v-model="tab">
        <v-tab> Create Room </v-tab>
        <v-tab> Select Room </v-tab>
      </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item v-for="item in items" :key="item" >
          </v-tab-item>
        </v-tabs-items>

        <h3>select</h3>
        <select v-model="selected">
          <option v-for="(room, i) in rooms" v-bind:key="i" v-bind:value="i">
          {{ room }}
        </option>
      </select>
      <!-- <button :onclick=>enter</button> -->
      <h3>create</h3>
      <input type="text" v-model="create_name" autocomplete="off"/> 
      <span v-if="room_exists"> 既に存在します </span>
      <!-- <button :onclick="createRoom()">create and enter</button> -->
  </div>
</template>

<style>
</style>

<script>
export default {
  data: function () {
    return {
      user_name: "",
      rooms: [],
      create_name: "",
      selected: "",
      room_exists: false,
      URL: "http://localhost:80/"
    }
  },
  created () {
    this.getRooms();
  },
  computed: {
  },
  watch: {
    create_name: function() {
      this.room_exists = this.rooms.indexOf(this.create_name) >= 0;
    },
  },
  methods: {
    getRooms: function() {
      fetch(this.URL + "rooms", {
        method: "GET",
      }).then(response => response.json())
      .then(json => {
        this.rooms = json.rooms;
      });
    },
    createRoom: function () {
      let room_name = document.getElementById( "room_name" ).value;
      let formData = new FormData();
      formData.append("room_name", room_name);
      // send it out
      let xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://localhost:80/rooms/' + room_name);
      xhr.responseType = 'json';
      xhr.send();
      xhr.onload = function() {
        let room_id =  xhr.response.room_id;
        let user_name = document.getElementById( "user_name" ).value;
        let xhr_second = new XMLHttpRequest();
        let json = JSON.stringify({
          "name": user_name,
          "room_id": room_id
        });
        xhr_second.open("POST", 'http://localhost:80/chat')
        xhr_second.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        xhr.responseType = 'document';
        xhr_second.send(json);
        xhr_second.onload = function() {
          let chat_dom = xhr_second.response;
          document.querySelector("body").innerHTML = chat_dom;
          // document.getElementById( "chat" ).innerHTML = chat_dom;
        };
      }
    }
  },
}
</script>
