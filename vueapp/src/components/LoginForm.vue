<template>
    <form @submit.prevent="">
        <div class="input-group">
            <label for="#nickname-input">Nickname</label>
            <input id="nickname-input" type="text" v-model="nickname">
        </div>
        <div class="input-group">
            <label for="#password-input">Password</label>
            <input id="password-input" type="password" v-model="password">
        </div>
        <hr>
        <button @click="login">Login</button>
    </form>
</template>

<script>
export default {
    setup() {
        
    },
    data() {
        return {
            nickname: this.$store.getters.getNickname,
            password: "",
        }
    },
    methods: {
        login(){
            const data = {username: this.nickname, password: this.password}
            this.$emit('submitForm', data)
        }
    }
}
</script>

<style lang="scss" scoped>
    .input-group{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 20px;
    }
</style>