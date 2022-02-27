<template>
    <form @submit.prevent="">
        <div class="input-group">
            <label for="#name-input">Name</label>
            <input id="name-input" type="text" v-model="name">
        </div>
        <div class="input-group">
            <label for="#password-input">Password</label>
            <input id="password-input" type="password" v-model="password">
        </div>
        <hr>
        <button @click="submitForm()">Save Settings</button>    
    </form>    
</template>

<script>
export default {
    setup() {
        
    },
    data(){
        return {
            name: "",
            password: "",
            cards: []
        }
    },
    methods: {
        submitForm(){
            console.log("submit")
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