<template>
    <form @submit.prevent="">
        <div class="input-group">
            <label for="#password-input">Password</label>
            <input id="password-input" type="text" v-model="password">
        </div>
        <hr>
        <button @click="sendPassword()">Send Password</button>
    </form>
</template>

<script>
export default {
    setup() {
        
    },
    data(){
        return {
            password: ""
        }
    },
    methods: {
        sendPassword(){
            this.$emit('submitForm', {password: this.password})
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