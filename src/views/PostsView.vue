<template>
    <h1 v-if="error != null" class="alert alert-danger" role="alert">
        {{ error }}
    </h1>
    <button v-else @click="$router.push('/posts/new')" type="button" style="float:right" width="200" id="Post" class="btn btn-primary">New Post</button>
    <div v-if="posts != null">
        <div class="cards">
            <div v-for="post in posts['posts']" class="card-columns">
                <div class="card" style="width: 35em;">
                    <a :href="/users/ + post['user_id'] ">
                        <div class="card-header">
                          <p><img :src="post['profilePhoto']" alt="Poster Profile Photo">{{ post['username'] }}</p>      
                        </div>
                    </a>
                    <div class="card-body">
                        <img :src="post['photo']" alt="Photo used in photo">
                        <br>
                        <br>
                        <p class="card-text">{{ post['caption'] }}</p>
                    </div>
                    <div class="card-footer clearfix">
                      
                        <div v-if="likes[post['id']-1][0]" @click="toggleLike(post['id'])" class="png-container">
                            <img src="/src/assets/like.png" alt="Like heart picture" class="red">
                        </div>
                        <div v-else @click="toggleLike(post['id'])" class="png-container">
                          <img src="/src/assets/like.png" alt="Like heart picture">
                          
                        </div>
                           
                        <p class="">{{ post['likes'] }} likes</p>
                        <p class="created">{{ post['created_on'] }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { jwtDecode } from "jwt-decode";
    import { ref, onMounted } from "vue";

    const likes = ref([]);
    const user_id = ref(null)
    const token = ref(null)
    const posts = ref(null);
    const error = ref(null)

    onMounted(() => {
        token.value = localStorage.getItem("token")
        if(token.value){
            if(localStorage.getItem('reloaded') == 'false'){
                localStorage.setItem('reloaded', 'true')
                window.location.reload()
            }
        }
        getPosts();
        getUserId();
    });

    function toggleLike(id){
        console.log(likes.value[id-1][0])
        fetch(`/api/v1/posts/${id}/like`, {
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
            error.value = data.error
            likes.value[id-1][0] = data.liked
            posts.value['posts'][id-1]['likes'] = data.likes
            console.log(posts.value['posts'][id-1])
        })
        .then(function (error) {
            console.log(error)
        });
    }

    function getUserId(){
        if (token.value){
            user_id.value = (jwtDecode(token.value).user_id || "null");
        }
    }

    function getPosts(){
        fetch('/api/v1/posts', {
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
            for(let arr in data['posts']){
                likes.value.push([
                    data['posts'][arr]['liked'],
                    data['posts'][arr]['id']])
            }
            error.value = data.error
            posts.value = data;
            console.log(data)
        })
        .then(function (error) {
            console.log(error)
        });
    }
</script>

<style>
 .png-container {
        overflow: hidden;
       
    }
    
    .red{
        filter: drop-shadow(0px 1000px 0 red);
        transform: translateY(-1000px);
    }
    p img{
        width:30px;
        height: 30px;
    }
  .card-header p {
  color:black; 
  
  
}
.card-body img {
 display: flex;
 flex-wrap: wrap;
  object-fit: cover; }

  .card {
  margin-bottom: 40px;
  width: 70px;
 
 }

 .card-footer img {

        width:30px;
        height: 30px;
        float: left;
        margin-right: 0%;
    }
.card-footer{
    display: flex;
    flex-direction: row;
}
  .created{
   margin-left: 350px;
  }
.card{
   
    overflow: hidden;
}
 
a{
    text-decoration: none;
}

#Post{
    width: 200px;
    margin-bottom: 20px;
}

</style>