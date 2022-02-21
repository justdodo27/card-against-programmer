<template>
    <main>
        <h3 v-show="$store.getters.getNickname != null">Logged in as {{ $store.getters.getNickname }}</h3>
        <ul>
            <li v-for="msg in messages" :key=msg>{{ msg }}</li>
        </ul>
        <button @click="send()">Send Message</button>
    </main>
</template>

<script>

export default {
    setup() {
        
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
            if (data.message)this.messages.push(data.message)
            else this.messages.push(data.tester)
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