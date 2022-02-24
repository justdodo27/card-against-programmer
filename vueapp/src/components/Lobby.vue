<template>
    <main id="lobby">
        <login-form @submit-form="login" v-if="$store.getters.getId == null"></login-form>
        <div v-else>
            <button @click="createGame()">Create Game</button>
            <button @click="logout">Logout</button>
        </div>
    </main>
</template>

<script>
import LoginForm from "./LoginForm.vue";


export default {
    setup() {
        
    },
    components: {
        LoginForm
    },
    data(){
        return {
            socket: new WebSocket(
                'ws://' +
                window.location.host +
                '/ws/game/'
            )
        }
    },
    methods: {
        login(event){
            this.socket.send(JSON.stringify({
                "type": "login",
                "username": event.username,
                "password": event.password
            }))
        },
        logout(){
            this.socket.send(JSON.stringify({
                "type": "logout"
            }))
            this.$store.commit('logout')
        },
        createGame(){
            const user_id = this.$store.getters.getId
            if (user_id) this.socket.send(JSON.stringify({
                "type": "create",
                "user": user_id
            }))
        }
    },
    created(){
        this.socket.onmessage = (e) => {
            console.log(e.data)
            const data = JSON.parse(e.data)
            if (data.error){
                window.alert(data.error)
            }else if(data.code){
                window.location += data.code + "/"
            }else{
                this.$store.commit('login', data)
            }
        }
    }
}
</script>

<style lang="scss">
    main#lobby {
        grid-row: 1/4;
        grid-column: 2/3;
        border: 1px solid black;
        border-top-left-radius: 20px;
        border-bottom-right-radius: 20px;
        padding: 10px 0px;
        display: grid;
        grid-template-columns: auto;
        grid-template-rows: 1fr;
        place-items: center;
    }

    
</style>