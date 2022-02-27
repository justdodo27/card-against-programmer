<template>
    <main>
        <login-form @submit-form="login" v-if="$store.getters.getId == null"></login-form>
        <div v-else>
        <game-form></game-form>
        <ul>
            <li v-for="msg in messages" :key=msg>{{ msg }}</li>
        </ul>
        <button @click="send()">Send Message</button>
        </div>
    </main>
</template>

<script>
import LoginForm from "./LoginForm.vue"
import GameForm from "./GameForm.vue"

export default {
    setup() {
        
    },
    components: {
        LoginForm, GameForm
    },
    data() {
        return {
            messages: [],
            gameSocket: null
        }
    },
    methods: {
        send(){
            console.log("CLICKED")
            this.gameSocket.send(JSON.stringify({
                'message': 'XDDD',
            }))
        },
        login(event){
            this.gameSocket.send(JSON.stringify({
                "type": "login",
                "username": event.username,
                "password": event.password
            }))
        },
        authenticate(id){
            this.gameSocket.send(JSON.stringify({
                "type": "authenticate",
                "user": id,
            }))
        }
    },
    mounted(){
        const roomCode = JSON.parse(document.querySelector("#room-json").textContent)
        this.gameSocket = new WebSocket(
            'ws://' +
            window.location.host +
            '/ws/game/' +
            roomCode +
            '/'
        )

        this.gameSocket.onmessage = (e) => {
            const data = JSON.parse(e.data)
            console.log(data)
            if (data.info && data.info == "authenticate"){
                const user = this.$store.getters.getId
                if (user){
                    this.authenticate(user)
                }
            }else if (data.info && data.info == "user"){
                const user = {"id": data.id, "username": data.username}
                this.$store.commit('login', user)
                this.authenticate(data.id)
            }else if (data.error){
                window.alert(data.error)
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    main{
        grid-row: 2/3;
        grid-column: 2/3;
    }
</style>