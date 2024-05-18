<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"><img src="/src/assets/photogram_logo.png" alt="Photogram Camera Logo">Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="/users/+myProfile()">My Profile</RouterLink>
            </li>
            <li v-if="token == null" class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li v-else class="nav-item">
              <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
  import { onMounted, ref } from "vue";
  import { jwtDecode } from "jwt-decode";
  import { RouterLink, useRouter } from "vue-router";

  // const router = useRouter()
  const token = ref(null)
  const user_id = ref(null)
  // const csrf_token = ref(null)

  onMounted(() =>{
    token.value = localStorage.getItem('token')
    if(!token.value){
      localStorage.setItem("reloaded", "false")
    }else{
      localStorage.setItem("reloaded", "true")
    }
  })

  // function logout(){
  //   localStorage.removeItem('token')
  //   token.value = localStorage.getItem('token')
  //   console.log(token.value)
  // }

  function myProfile(){
    token.value = localStorage.getItem('token')
    if (token.value){
        user_id.value = (jwtDecode(token.value).user_id);
    }
    console.log(user_id.value)
    return user_id.value
  }

  // function getCsrf(){
  //       fetch('/api/v1/csrf-token')
  //       .then((response) => response.json())
  //       .then((data) => {
  //           console.log(data)
  //           csrf_token.value = data.csrf_token;
  //       })
  //   }
</script>

<style>
/* Add any component specific styles here */
  div#navbarSupportedContent {
    flex-grow: unset;
  }

  a.navbar-brand img {
    height: 20px;
    width: 20px;
  }
  .navbar{
    margin-bottom:10%;
  }
</style>