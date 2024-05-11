<template>
    <h1 v-if="error != null" class="alert alert-danger" role="alert">{{ error }}</h1>
    <div v-if="user != null" class="container">
        <div class="profile-top">
            <img :src="user['profile_photo']" alt="profile Profile Photo" class="card-img-left">
            <div class="profile-top-middle">
                <p  id= "name" class="card-text">{{ user['firstname'] +" "+ user['lastname']}}</p>
                <p class="card-text">{{ user['location'] }}</p>
                <p class="card-text"> Memeber since {{ user['joined_on'] }}</p>
                <p class="card-text">{{ user['biography'] }}</p>
            </div>
            <div class=" profile-right">
                <div class="profile-posts">
                    <p class="count">{{ user['postcount'] }} </p>
                    <p class=" description" > Posts </p>
                </div>
                <div class="profile-followers">
                        <p class="count">{{ followers }} </p>
                        <p class=" description" >Followers</p>
                </div>
            <div class="buttons">
                    <button v-if="followed" @click="toggleFollow" id="Follow" class="btn btn-success">Following</button>
                    <button v-else @click="toggleFollow" id="Follow" class="btn btn-primary">Follow</button>
            </div>   
               
        </div>
        
            
          
        </div>
        <div v-if="posts != null" class="images">
            <div v-for="post in posts" class="card">
                <img :src="post['photo']" alt="Post Image" class="card-img-top">
            </div>
        </div>
        <h1 v-else class="alert alert-danger" role="alert">{{ message }}</h1>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";

    const route = useRoute()
    const followers = ref(null)
    const followed = ref(null)
    const token = ref(null)
    const posts = ref(null)
    const error = ref(null)
    const user = ref(null)
    const message = ref(null)

    onMounted(() => {
        token.value = localStorage.getItem("token")
        getUser();
    });

    function toggleFollow(){
        fetch(`/api/v1/users/${route.params.user_id}/follow`, {
            // method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            console.log(data)
            followed.value = data.followed
            followers.value = data.followers
        })
        .then(function (error) {
            console.log(error)
        });
    }

    function getUser() {
        fetch(`/api/v1/users/${route.params.user_id}/posts`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        })
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            console.log(data)
            // console.log()
            posts.value = data.posts
            user.value  = data.user
            followers.value = data.followers
            followed.value = data.followed
            error.value = data.error
            message.value = data.message

            console.log(message.value,posts.value)
        })
        .then(function (error) {
            console.log(error)
        });
    }
</script>
<style>
.profile-top{
    margin-top: 0px;
    display: flex;
    flex-direction: row;
    border: 2px solid lightgrey;
    border-radius: 5px;
    margin-bottom: 30px;
    width: 60em;
    
}

.profile-top img{
    height: 200px;
    width: 200px;
    
}
.profile-posts{
    margin-left: 100px;
}
.profile-followers{
    margin-left: 20px;
    
}
#Follow{
    width: 150px;
}
#name{
    font-size: 25px;
    font-weight: bold;
    color: Black;
}
.profile-top-middle{
    color: gray;
}
.description{
    color: grey;
    font-weight: bold;
    font-size: 20px;
}
.count{
    color:black;
    font-weight: bold;
    font-size: 25px;
}
.profile-right {
    display: flex;
    flex-direction: row;
    
}

.button{
    display: flex;
    flex-direction: column;
}

.images {
    display: grid;
    grid-template-columns: repeat(3, 1fr); 
    gap: 20px;
    width: 60em
}

.card-img-top {
    width: 100%;
    height: 250px;
    
}
</style>