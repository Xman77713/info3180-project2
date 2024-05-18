<script setup>
  const welcomeMessage = "Share photos of your favourite moments with friends, family and the world.";
</script>

<template>
  <div class="container d-flex">
    <img src="/src/assets/home_image.jpg" alt="Home Page Image">
    <div id="welcome" class="border shadow p-3 bg-white rounded ">
      <div class="text-center">
        <div>
         <h1> <img src="/src/assets/photogram_logo.png" alt="Phorogram Camera Logo"> Photogram</h1>
          
        </div>
        <hr>
        
        <p>{{ welcomeMessage }}</p>
        <div class="buttons">
          <button @click="$router.push('/register')" type="button" class="btn btn-secondary neon-green">Register</button>
          <button @click="$router.push('/login')" type="button" class="btn btn-secondary aqua-blue">Login</button>
        </div>
      </div>
    </div>
  </div>

</template>

<style>

  body {
    padding-top: 0;
  }

  div.text-center img {
   
    height: 30px;
    width: 30px;
   
  }

  img {
    height: 300px;
    width:500px;
    margin-right: 20px;
    border-radius: 5px;
  }

  .neon-green {
  background-color: #39FF14;
  border: none;
  width:150px;
  margin-right: 20px;
  }
  .aqua-blue{
  background-color:blue ;
  border: none;
  width:150px;
  }
  h1 {
  font-family: 'Brush Script MT', 'Brush Script Std', cursive;
  font-size: 30px;
}
p{
  text-align: left;
}
</style>