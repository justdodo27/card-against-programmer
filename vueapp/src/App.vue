<template>
  <div class="container">
    <lobby v-show="$store.getters.getNickname == null"></lobby>
    <game v-show="$store.getters.getNickname != null"></game>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import Lobby from "./components/Lobby.vue"
import Game from "./components/Game.vue"

export default {
  name: "App",
  components: {
    Lobby, Game
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
  width: 100%;
}

.container{
  display: grid;
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: 1fr 3fr 1fr;
  height: 100vh;
  place-items: center;
}

button{
  font-size: 100%;
  padding: 10px;
  border: none;
  border-radius: 2px;
  color: lighten(purple, 10%);
  background-color: lighten(purple, 50%);
  transition: all 0.1s ease-out;
}

button:hover{
  cursor: pointer;
}

button:active{
  color: lighten(purple, 50%);
  background-color: lighten(purple, 10%);
}
</style>
