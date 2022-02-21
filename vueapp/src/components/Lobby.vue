<template>
    <main>
        <form @submit.prevent="">
            <div class="input-group">
                <label for="#nickname-input">Nickname</label>
                <input id="nickname-input" type="text" v-model="nickname">
            </div>
            <hr>
            <button @click="login">Join game</button>
        </form>
        <h1>{{ nickname }}</h1>
    </main>
</template>

<script>
export default {
    setup() {
        
    },
    data() {
        return {
            nickname: this.$store.getters.getNickname
        }
    },
    methods: {
        login(){
            this.$store.commit('setnickname', {nickname: this.nickname})
            console.log(this.$store.getters.getNickname)
        }
    }
}
</script>

<style lang="scss">
    main {
        grid-row: 2/3;
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

    .input-group{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 20px;
    }
</style>