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
        <div>
        <button @click="submitForm()">Save Settings</button>    
        <button>Start Game</button>
        </div>
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
            const data = {
                name: this.name,
                password: this.password,
                cards: this.cards
            }
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

    form{
        grid-column: 2/3;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    hr{
        width: 100%;
    }
</style>