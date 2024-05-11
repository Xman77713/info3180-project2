<script setup>
import { ref, onMounted } from "vue";

const csrf_token = ref("");
const msg = ref(null);

onMounted(() =>{
    getCsrf()
});

function getCsrf(){
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        csrf_token.value = data.csrf_token;
    })
}

function registerUser(){
    let registerForm = document.getElementById('registerForm');
    let form_data = new FormData(registerForm);

    fetch('/api/v1/register', {
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
        msg.value = data;
    })
    .catch(function (error) {
        console.log(error)
    });
}
</script>
<template>
  <div class="container">

  <div v-if="msg != null">
        <div v-if="msg['errors']" class="alert alert-danger" role="alert">
            <li v-for="err in msg['errors']"> {{ err }} </li>
        </div>
        <div v-else class="alert alert-success" role="alert">
            <p>{{ msg['message'] }}</p>
        </div>
    </div>
    <h1>Register</h1>
    <form @submit.prevent="registerUser" method="POST" id="registerForm" enctype="multipart/form-data">
        <div class="form-group mb-3">
            <label for="firstname" class="form-label">First Name</label>
            <input id="firstname" name = "firstname" type="text" class="form-control" placeholder="Please enter your First Name">
        </div>
        <div class="form-group mb-3">
            <label for="lastname" class="form-label">Last Name</label>
            <input id="lastname" name = "lastname" type="text" class="form-control" placeholder="Please enter your Last Name">
        </div>
        <div class="form-group mb-3">
            <label for="email" class="form-label">Email Address</label>
            <input id="email" name = "email" type="text" class="form-control" placeholder="Please enter your Email Address">
        </div>
        <div class="form-group mb-3">
            <label for="username" class="form-label">Username</label>
            <input id="username" name = "username" type="text" class="form-control" placeholder="Please enter your Username">
        </div>
        <div class="form-group mb-3">
            <label for="password" class="form-label">Password</label>
            <input id="password" name = "password" type="text" class="form-control" placeholder="Please enter your Password">
        </div>
        <div class="form-group mb-3">
            <label for="location" class="form-label">Location</label>
            <input id="location" name = "location" type="text" class="form-control" placeholder="Please enter your Location">
        </div>
        <div class="form-group mb-3">
            <label for="biography" class="form-label">Biography</label>
            <input id="biography" name = "biography" type="text" class="form-control" placeholder="Please enter your Biography">
        </div>
        <div class="form-group mb-3">
            <label for="profile_photo" class="form-label">Profile Photo</label>
            <input id="profile_photo" name = "profile_photo" type="file" class="form-control">
        </div>
        <button class="btn btn-primary" type="submit">Register</button>
    </form>
</div> 
</template>


<style>

</style>