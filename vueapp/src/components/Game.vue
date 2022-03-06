<template>
    <main>
        <login-form @submit-form="login" v-if="$store.getters.getId == null"></login-form>
        <password-form @submit-form="sendPassword" v-else-if="passwordNeeded"></password-form>
        <div v-else class="game-menu">
        <game-form @submit-form="saveSettings" v-if="showForm"></game-form>
        <chat v-model:players="players" v-model:messages="messages" @message-send="send"></chat>
        </div>
    </main>
</template>

<script>
import LoginForm from "./LoginForm.vue"
import GameForm from "./GameForm.vue"
import PasswordForm from "./PasswordForm.vue"
import Chat from './Chat.vue'


export default {
    setup() {
        
    },
    components: {
        LoginForm, GameForm, PasswordForm,
        Chat
    },
    data() {
        return {
            messages: [],
            gameSocket: null,
            showForm: false,
            passwordNeeded: false,
            players: [],
        }
    },
    methods: {
        send(event){
            const message = {
                "type": "message",
                "message": event
            }
            this.gameSocket.send(JSON.stringify(message))
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
        },
        saveSettings(event){
            this.gameSocket.send(JSON.stringify({
                "type": "config",
                ...event
            }))
        },
        sendPassword(event){
            this.gameSocket.send(JSON.stringify({
                "type": "password",
                ...event
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
            if (data.info && data.info == "authenticate"){
                const user = this.$store.getters.getId
                if (user){
                    this.authenticate(user)
                }
            }else if (data.info && data.info == "user"){
                const user = {"id": data.id, "username": data.username}
                this.$store.commit('login', user)
                this.authenticate(data.id)
            }else if (data.info && data.info == "password"){
                this.passwordNeeded = true
            }else if (data.info && data.info == "ok"){
                this.passwordNeeded = false
            }else if (data.info && data.info == "refresh"){
                this.players = data.players
            }else if (data.creator){
                this.showForm = true
            }else if (data.error){
                window.alert(data.error)
            }else if (data.message){
                this.messages.push(data)
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    main{
        width: 100%;
        height: 100%;
        grid-row: 1/4;
        grid-column: 1/4;
    }

    .game-menu{
        width: 100%;
        height: 100%;
        display: grid;
        grid-template: 50% 50% / 20% 60% 20%;
    }
</style>