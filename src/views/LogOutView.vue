<template>
    <h1 v-if="message != null" class="alert alert-success" role="alert">
        {{ message }}
    </h1>
</template>

<script setup>
    import { onMounted, ref } from "vue";

    const csrf_token = ref(null)
    const message = ref(null)

    onMounted(() =>{
        if(localStorage.getItem('reloaded') == 'true'){
            getCsrf()
        }else{
            message.value = 'Logged Out Successfully'
        }
    })

    function logout(){
        fetch('/api/v1/auth/logout', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token.value
            }
            })
            .then(function (response) {
                return response.json()
            })
            .then(function (data) {
                console.log(data)
                localStorage.removeItem('token')
                localStorage.removeItem('reloaded', 'false')
                window.location.reload()
            })
            .then(function (error) {
                console.log(error)
        });
    }

    function getCsrf(){
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            csrf_token.value = data.csrf_token;
            logout()
        })
    }
</script>