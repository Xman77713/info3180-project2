<!-- Patrick actually committed this thorugh alex laptop, glitches happening on the mac-->
<template>
    <div v-if="msg != null">
        <div v-if="msg['errors']" class="alert alert-danger" role="alert">
            <p> {{ msg['errors'] }} </p>
        </div>
        <div v-else class="alert alert-success" role="alert">
            <p>{{ msg['message'] }}</p>
        </div>
    </div>
    <h1>Login</h1>
    <form @submit.prevent="login" method="post" id="loginForm">
        <div class="form-group mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" name="username" class="form-control" placeholder="Please enter your username">
        </div>
        <div class="form-group mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="text" name="password" class="form-control" placeholder="Please enter your password">
        </div>
        <button class="btn btn-primary" type="submit">Login</button>
    </form>
</template>

<style>
    body {
        background-color: #F6F0E6;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
    }


    h1{
        align-content: left;
        font-weight: bold;
        font-size: 150%;
        padding-bottom: 20px; 
    }

    #loginForm{
        background-color: white;
        border: 0.5px solid black;
        /* border-bottom:none; */
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        padding: 30px;
        padding-bottom: 1;
        border-radius: 1px;
        width: 400px;
        height: 300px;
    }

    .btn-primary {
        background-color:#70bb1f;
        width: 100%;
    }
    
    .form-label{
        font-weight: bold;
    }
</style>

<script setup>
    import { ref, onMounted } from "vue";
    import { useRouter } from "vue-router";

    onMounted(() =>{
        getCsrf();
    });

    const msg = ref(null)
    const router = useRouter();
    const csrf_token = ref("")

    function getCsrf(){
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            csrf_token.value = data.csrf_token;
        })
    }

    function login(){
        let loginForm = document.getElementById('loginForm')
        let form_data = new FormData(loginForm);

        fetch('/api/v1/auth/login', {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data){
            console.log(data)
            msg.value = data;

            if(msg.value['token']){
                localStorage.setItem('token', msg.value['token'])
                router.replace({ path: '/explore' })
            }
        })
        .catch(function (error) {
            console.log(error)
        });
    }
</script>
