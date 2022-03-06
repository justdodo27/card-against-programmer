<template>
    <div class="side-panel">
        <div class="players">
            <div v-for="player in playersUpdate" :key="player">
                {{ player }}
            </div>
        </div>
        <div class="chat">
            <div class="messages">
                <div class="message" v-for="message in messagesUpdate" :key="message">
                    <span>{{ message.user }}:</span> {{ message.message }}
                </div>
            </div>
            <div class="chat-input">
                <input type="text" v-model="messageBuffer">
                <button class="send-btn" @click="sendMsg()">SEND</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    setup() {
        
    },
    props: {
        players: Array,
        messages: Array,
    },
    data() {
        return {
            messageBuffer: ""
        }
    },
    computed: {
        playersUpdate(){
            return this.players
        },
        messagesUpdate(){
            return this.messages
        }
    },
    methods: {
        sendMsg(){
            this.$emit('messageSend', this.messageBuffer)
            this.messageBuffer = ""
        }
    }
}
</script>

<style lang="scss" scoped>
    .side-panel{
        grid-column: 1/4;
        grid-row: 2/3;
        display: grid;
        grid-template: 100% / 200px auto;
        background-color: gray;
        margin-bottom: 10px;
    }

    .chat{
        width: 100%;
        height: 100%;
        background-color: green;
        display: grid;
        grid-template: auto 30px / 100%;
    }

    .chat-input{
        height: 100%;
        display: flex;
    }

    .chat-input .send-btn{
        padding: none;
        background-color: none;
    }

    .chat-input input{
        flex-grow: 2;
    }

    .chat .messages{
        overflow-y: scroll;
    }

    .message{
        width: 100%;
        text-align: start;
        text-indent: 10px;
        border-bottom: 1px solid blue;
    }

    .message span{
        font-weight: bold;
    }
</style>